import uuid
from fastapi import Form, UploadFile, File

from src.exeptions import QuestionNotFoundException
from src.schemas.questions import QuestionPatchDTO, QuestionAddDTO
from src.services.base import BaseService


class QuestionsService(BaseService):
    async def create_questions(
        self,
        title_ru: str = Form(None),
        title_kg: str = Form(None),
        description_ru: str = Form(None),
        description_kg: str = Form(None),
        ticket_id: uuid.UUID = Form(None),
        theme_id: uuid.UUID = Form(None),
        files: list[UploadFile] = File(None),
    ):
        filenames = []
        if files:
            for file in files:
                saved_filename = await self.db.questions.save_photo(file)
                filenames.append(saved_filename)

        new_questions = QuestionAddDTO(
            id=uuid.uuid4(),
            title_ru=title_ru,
            title_kg=title_kg,
            description_ru=description_ru,
            description_kg=description_kg,
            ticket_id=ticket_id,
            theme_id=theme_id,
            files=filenames,
        )
        await self.db.questions.add(new_questions)
        await self.db.commit()
        return new_questions

    async def get_questions(self):
        questions = await self.db.questions.get_all()
        return questions

    async def get_by_questions_id(self, question_id: uuid.UUID):
        questions = await self.db.questions.get_one_or_none(id=question_id)
        return questions

    async def get_questions_by_ticket_id(self, ticket_id: uuid.UUID):
        questions = await self.db.questions.get_questions_by_ticket_id(ticket_id)
        return questions

    async def get_random_questions(self):
        random_questions = await self.db.questions.get_random_questions()
        return random_questions

    async def patch_questions(
        self, question_id: uuid.UUID, data: QuestionPatchDTO, exclude_unset: bool = False
    ):
        questions = await self.db.questions.get_one_or_none(id=question_id)
        if not questions:
            raise QuestionNotFoundException
        await self.db.questions.edit_patch(data, exclude_unset=exclude_unset, id=question_id)
        await self.db.commit()
        return questions

    async def delete_question(self, question_id: uuid.UUID):
        await self.db.questions.delete(id=question_id)
        await self.db.commit()

    async def patch_questions_file(
        self, question_id: uuid.UUID, files: list[UploadFile] = File(None)
    ):
        questions = await self.db.questions.get_one_or_none(id=question_id)
        if not questions:
            raise QuestionNotFoundException
        if files:
            new_filenames = await self.db.questions.upload_files(files)
            questions.files = new_filenames
        await self.db.questions.update(questions)
        await self.db.commit()
        return questions

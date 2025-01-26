import uuid
from typing import List, Optional

from src.exeptions import AnswerNotFoundException
from src.schemas.answers import AnswerAddDTO, AnswerPatchDTO, AnswerAddRequestDTO, AnswerResponseDTO
from src.services.base import BaseService


class AnswersService(BaseService):
    async def create_answers(self, data: AnswerAddRequestDTO) -> AnswerAddDTO:
        new_answers = AnswerAddDTO(
            id=uuid.uuid4(),
            title_ru=data.title_ru,
            title_kg=data.title_kg,
            is_correct=data.is_correct,
            question_id=data.question_id,
        )
        await self.db.answers.add(new_answers)
        await self.db.commit()
        return new_answers

    async def get_answers(self) -> List[AnswerResponseDTO]:
        answers = await self.db.answers.get_all()
        return answers

    async def get_answer_id(self, answer_id: uuid.UUID) -> AnswerResponseDTO:
        answers = await self.db.answers.get_one(id=answer_id)
        return answers

    async def get_answers_by_question_id(self, question_id: uuid.UUID) -> List[AnswerResponseDTO]:
        answers_by_questions = await self.db.answers.get_answers_by_question_id(
            question_id=question_id
        )
        return answers_by_questions

    async def patch_answers(
        self, answer_id: uuid.UUID, data: AnswerPatchDTO, exclude_unset: bool = False
    ) -> Optional[AnswerResponseDTO]:
        answers = await self.db.answers.get_one_or_none(id=answer_id)
        if not answers:
            raise AnswerNotFoundException
        await self.db.answers.edit_patch(data, exclude_unset=exclude_unset, id=answer_id)
        await self.db.commit()
        return answers

    async def delete_answer(self, answer_id: uuid.UUID) -> None:
        answers = await self.db.answers.get_one_or_none(id=answer_id)
        if not answers:
            raise AnswerNotFoundException
        await self.db.answers.delete(id=answer_id)
        await self.db.commit()

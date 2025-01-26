import uuid

from src.exeptions import ThemeNotFoundException
from src.schemas.themes import ThemeAddRequestDTO, ThemeAddDTO, ThemePatchDTO
from src.services.base import BaseService


class ThemesService(BaseService):
    async def create_themes(self, data: ThemeAddRequestDTO):
        new_themes = ThemeAddDTO(
            id=uuid.uuid4(),
            title_ru=data.title_ru,
            title_kg=data.title_kg,
        )
        await self.db.themes.add(new_themes)
        await self.db.commit()
        return new_themes

    async def get_themes_by_id(self, theme_id: uuid.UUID):
        themes = await self.db.themes.get_one_or_none(id=theme_id)
        return themes

    async def get_theme(self):
        themes = await self.db.themes.get_all()
        return themes

    async def patch_theme(
        self, theme_id: uuid.UUID, data: ThemePatchDTO, exclude_unset: bool = False
    ):
        themes = await self.db.themes.get_one_or_none(id=theme_id)
        if not themes:
            raise ThemeNotFoundException
        await self.db.themes.edit_patch(data, exclude_unset=exclude_unset, id=theme_id)
        await self.db.commit()
        return themes

    async def delete_theme(self, theme_id: uuid.UUID):
        await self.db.themes.delete(id=theme_id)
        await self.db.commit()

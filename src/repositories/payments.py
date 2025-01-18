import uuid
from sqlalchemy import select

from src.models.payments import PaymentOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import PaymentDataMapper


class PaymentsRepository(BaseRepository):
    model = PaymentOrm
    mapper = PaymentDataMapper

    async def get_payments_by_user_id(self, user_id: uuid.UUID):
        query = select(self.model).where(self.model.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalars().all()

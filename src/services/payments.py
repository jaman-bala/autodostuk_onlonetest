import uuid

from src.exeptions import PaymentNotFoundException
from src.schemas.payments import PaymentAddRequestDTO, PaymentPatchDTO, PaymentAddDTO
from src.services.base import BaseService


class PaymentsService(BaseService):
    async def create_payments(self, data: PaymentAddRequestDTO):
        new_payments = PaymentAddDTO(
            id=uuid.uuid4(),
            user_id=data.user_id,
            date_check=data.date_check,
            price=data.price,
        )
        await self.db.payments.add(new_payments)
        await self.db.commit()
        return new_payments

    async def get_payments(self):
        payments = await self.db.payments.get_all()
        return payments

    async def get_payment_by_id(self, payment_id: uuid.UUID):
        payments = await self.db.payments.get_one_or_none(id=payment_id)
        return payments

    async def patch_payments(
        self, payment_id: uuid.UUID, data: PaymentPatchDTO, exclude_unset: bool = False
    ):
        payments = await self.db.payments.get_one_or_none(id=payment_id)
        if not payments:
            raise PaymentNotFoundException
        await self.db.payments.edit_patch(data, exclude_unset=exclude_unset, id=payment_id)
        await self.db.commit()
        return payments

    async def delete_payments(self, payment_id: uuid.UUID):
        await self.db.payments.delete(id=payment_id)
        await self.db.commit()

    async def get_payments_by_user_id(self, user_id: uuid.UUID):
        payments = await self.db.payments.get_payments_by_user_id(user_id)
        return payments

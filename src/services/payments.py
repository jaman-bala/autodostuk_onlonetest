import uuid

from src.exeptions import PaymentNotFoundException
from src.schemas.payments import PaymentAddRequest, PaymentPatch, PaymentAdd
from src.services.base import BaseService


class PaymentsService(BaseService):
    async def create_payments(self, data: PaymentAddRequest):
        new_payment = PaymentAdd(
            id=uuid.uuid4(),
            user_id=data.user_id,
            date_check=data.date_check,
            price=data.price,
        )
        await self.db.payments.add(new_payment)
        await self.db.commit()
        return new_payment

    async def get_payments(self):
        payment = await self.db.payments.get_all()
        return payment

    async def get_payment_by_id(self, payment_id: uuid.UUID):
        payments = await self.db.payments.get_one_or_none(id=payment_id)
        return payments

    async def patch_payments(
        self, payment_id: uuid.UUID, data: PaymentPatch, exclude_unset: bool = False
    ):
        payment = await self.db.payments.get_one_or_none(id=payment_id)
        if not payment:
            raise PaymentNotFoundException
        await self.db.payments.edit_patch(data, exclude_unset=exclude_unset, id=payment_id)
        await self.db.commit()

    async def delete_payments(self, payment_id: uuid.UUID):
        await self.db.payments.delete(id=payment_id)
        await self.db.commit()

    async def get_payments_by_user_id(self, user_id: uuid.UUID):
        payments = await self.db.payments.get_payments_by_user_id(user_id)
        return payments

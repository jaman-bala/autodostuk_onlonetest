import uuid

from src.exeptions import TicketNotFoundException
from src.schemas.tickets import TicketAdd, TicketAddRequest, TicketPatch
from src.services.base import BaseService


class TicketsService(BaseService):
    async def create_tickets(self, data: TicketAddRequest):
        create_ticket = TicketAdd(
            id=uuid.uuid4(),
            title=data.title,
        )
        await self.db.tickets.add(create_ticket)
        await self.db.commit()
        return create_ticket

    async def get_tickets(self):
        tickets = await self.db.tickets.get_all()
        return tickets

    async def get_tickets_by_id(self, ticket_id: uuid.UUID):
        tickets = await self.db.tickets.get_one_or_none(id=ticket_id)
        return tickets

    async def patch_ticket(
        self, ticket_id: uuid.UUID, data: TicketPatch, exclude_unset: bool = False
    ):
        ticket = await self.db.tickets.get_one_or_none(id=ticket_id)
        if not ticket:
            raise TicketNotFoundException
        await self.db.tickets.edit_patch(data, exclude_unset=exclude_unset, id=ticket_id)
        await self.db.commit()
        return ticket

    async def delete_ticket(self, ticket_id: uuid.UUID):
        await self.db.tickets.delete(id=ticket_id)
        await self.db.commit()

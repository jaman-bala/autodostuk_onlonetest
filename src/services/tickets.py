import uuid

from src.exeptions import TicketNotFoundException
from src.schemas.tickets import TicketAddDTO, TicketAddRequestDTO, TicketPatchDTO
from src.services.base import BaseService


class TicketsService(BaseService):
    async def create_tickets(self, data: TicketAddRequestDTO):
        create_ticket = TicketAddDTO(
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
        self, ticket_id: uuid.UUID, data: TicketPatchDTO, exclude_unset: bool = False
    ):
        tickets = await self.db.tickets.get_one_or_none(id=ticket_id)
        if not tickets:
            raise TicketNotFoundException
        await self.db.tickets.edit_patch(data, exclude_unset=exclude_unset, id=ticket_id)
        await self.db.commit()
        return tickets

    async def delete_ticket(self, ticket_id: uuid.UUID):
        await self.db.tickets.delete(id=ticket_id)
        await self.db.commit()

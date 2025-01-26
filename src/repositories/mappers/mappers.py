from src.repositories.mappers.base import DataMapper

from src.models.users import UsersOrm
from src.models.images import AvatarOrm, ImagesOrm
from src.models.questions import QuestionOrm
from src.models.answers import AnswerOrm
from src.models import GroupOrm
from src.models import TicketOrm
from src.models import TotalOrm
from src.models import ThemeOrm
from src.models.payments import PaymentOrm
from src.models.reports import ReportOrm

from src.schemas.answers import AnswerDTO
from src.schemas.avatars import AvatarDTO, ImagesDTO
from src.schemas.group import GroupDTO
from src.schemas.payments import PaymentDTO
from src.schemas.questions import QuestionDTO
from src.schemas.reports import ReportDTO
from src.schemas.themes import ThemeDTO
from src.schemas.tickets import TicketDTO
from src.schemas.totals import TotalDTO
from src.schemas.users import UserDTO


class UserDataMapper(DataMapper):
    db_model = UsersOrm
    schema = UserDTO


class AvatarDataMapper(DataMapper):
    db_model = AvatarOrm
    schema = AvatarDTO


class ImageDataMapper(DataMapper):
    db_model = ImagesOrm
    schema = ImagesDTO


class QuestionDataMapper(DataMapper):
    db_model = QuestionOrm
    schema = QuestionDTO


class AnswerDataMapper(DataMapper):
    db_model = AnswerOrm
    schema = AnswerDTO


class GroupDataMapper(DataMapper):
    db_model = GroupOrm
    schema = GroupDTO


class TicketDataMapper(DataMapper):
    db_model = TicketOrm
    schema = TicketDTO


class TotalDataMapper(DataMapper):
    db_model = TotalOrm
    schema = TotalDTO


class ThemeDataMapper(DataMapper):
    db_model = ThemeOrm
    schema = ThemeDTO


class PaymentDataMapper(DataMapper):
    db_model = PaymentOrm
    schema = PaymentDTO


class ReportDataMapper(DataMapper):
    db_model = ReportOrm
    schema = ReportDTO

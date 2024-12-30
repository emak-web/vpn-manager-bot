from aiogram.filters import BaseFilter
from aiogram.types import Message
from services.db_connector import db


class IsAuthorizedUserFilter(BaseFilter):
    
    def __init__(self, is_user):
        self.is_user = is_user

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in db.get_user_id_list()

from aiogram.filters import BaseFilter
from aiogram.types import Message
from config.config import env


class IsAdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in env.admins

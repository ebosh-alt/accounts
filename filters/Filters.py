from aiogram.filters import Filter
from aiogram.types import Message, User
from data.config import ADMINS


class IsAdmin(Filter):
    async def __call__(self, message: Message, event_from_user: User) -> bool:
        if event_from_user.id in ADMINS:
            return True
        return False

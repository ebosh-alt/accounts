import logging
from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import Column, String, BigInteger

from . import Deal
from .accounts import Accounts

from .base import Base, BaseDB

from ..models import DataDeals

logger = logging.getLogger(__name__)


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    username = Column(String)

    def dict(self):
        return {"id": self.id,
                "username": self.username,
                }


class Users(BaseDB):
    async def new(self, user: User):
        await self._add_obj(user)

    async def get(self, id: int) -> User | None:
        result = await self._get_object(User, id)
        return result

    async def update(self, user: User) -> None:
        await self._update_obj(instance=user, obj=User)

    async def delete(self, user: User) -> None:
        await self._delete_obj(instance=user)

    async def in_(self, id: int) -> User | bool:
        result = await self.get(id)
        if type(result) is User:
            return result
        return False

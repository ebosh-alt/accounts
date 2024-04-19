import logging

from sqlalchemy import Column, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base, BaseDB

logger = logging.getLogger(__name__)


class Chat(Base):
    __tablename__ = "chats"

    id: int = Column(BigInteger, primary_key=True)
    user_id: int = Column(BigInteger, ForeignKey("users.id"))
    seller_id: id = Column(BigInteger, ForeignKey("sellers.id"))
    # user = relationship("User", back_populates="chats")
    # seller = relationship("Seller", back_populates="chats")

    def dict(self):
        return {"id": self.id,
                "user_id": self.user_id,
                "seller_id": self.seller_id,
                "user": self.user.dict(),
                "seller": self.seller.dict(),
                }


class Chats(BaseDB):
    async def new(self, chat: Chat):
        await self._add_obj(chat)

    async def get(self, id: int) -> Chat | None:
        result = await self._get_obj(Chat, id)
        return result

    async def update(self, chat: Chat) -> None:
        await self._update_obj(instance=chat, obj=Chat)

    async def delete(self, chat: Chat) -> None:
        await self._delete_obj(instance=chat)

    async def in_(self, id: int) -> Chat | bool:
        result = await self.get(id)
        if result is Chat:
            return result
        return False

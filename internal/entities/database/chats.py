import logging

from sqlalchemy import Column, BigInteger, ForeignKey

from .base import Base, BaseDB

logger = logging.getLogger(__name__)


class Chat(Base):
    __tablename__ = "chats"

    id: int = Column(BigInteger, primary_key=True)
    user_id: int = Column(BigInteger, ForeignKey("users.id"))
    seller_id: int = Column(BigInteger, ForeignKey("sellers.id"))

    def dict(self):
        return {"id": self.id,
                "user_id": self.user_id,
                "seller_id": self.seller_id
                }


class Chats(BaseDB):
    async def new(self, chat: Chat):
        await self._add_obj(chat)

    async def get(self, id: int) -> Chat | None:
        result = await self._get_object(Chat, id)
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
    
    async def get_chat_by_user(self, user_id: int) -> Chat | None:
        filters = {Chat.user_id: user_id}
        result: list[Chat] = await self._get_objects(Chat, filters=filters)
        if len(result) > 0:
            chat = result[0]
            return chat
        return None

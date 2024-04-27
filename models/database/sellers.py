import logging
from sqlalchemy import Column, String, Boolean, FLOAT, Integer, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from data.config import SELLER
from .base import Base, BaseDB

logger = logging.getLogger(__name__)


class Seller(Base):
    __tablename__ = "sellers"

    id = Column(BigInteger, primary_key=True)
    rating = Column(BigInteger)
    balance = Column(BigInteger)
    username = Column(String)

    def dict(self):
        return {"id": self.id,
                "rating": self.rating,
                "balance": self.balance,
                "username": self.username,
                }


class Sellers(BaseDB):
    async def new(self, seller: Seller):
        await self._add_obj(seller)

    async def get(self, id: int = None) -> Seller | None:
        if id is None:
            id = SELLER
        result = await self._get_object(Seller, id)
        return result

    async def update(self, seller: Seller) -> None:
        await self._update_obj(instance=seller, obj=Seller)

    async def delete(self, seller: Seller) -> None:
        await self._delete_obj(instance=Seller)

    async def in_(self, id: int) -> Seller | bool:
        result = await self.get(id)
        if result is Seller:
            return result
        return False

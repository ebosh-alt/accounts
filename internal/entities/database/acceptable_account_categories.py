import logging

from sqlalchemy import Column, String, Integer

from .base import Base, BaseDB

logger = logging.getLogger(__name__)


class AcceptableAccountCategory(Base):
    __tablename__ = "acceptable_account_categories"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)

    def dict(self):
        return {"id": self.id,
                "name": self.name,
                }

class AcceptableAccountCategories(BaseDB):
    def __init__(self):
        super().__init__(AcceptableAccountCategory)

    async def new(self, instance: AcceptableAccountCategory):
        await self._add_obj(instance)

    async def get(self, id: int) -> AcceptableAccountCategory | None:
        result = await self._get_object(id)
        return result

    async def update(self, instance: AcceptableAccountCategory) -> None:
        await self._update_obj(instance=instance)

    async def delete(self, instance: AcceptableAccountCategory) -> None:
        await self._delete_obj(instance=instance)

    async def in_(self, id: int) -> AcceptableAccountCategory | bool:
        result = await self.get(id)
        if type(result) is AcceptableAccountCategory:
            return result
        return False

    async def get_all_name_types(self):
        result = []
        async for acc_type in self:
            result.append(acc_type.name)
        return result
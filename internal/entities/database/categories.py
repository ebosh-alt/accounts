import logging

from sqlalchemy import Column, String, Integer

from .base import Base, BaseDB

logger = logging.getLogger(__name__)


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)

    def dict(self):
        return {"id": self.id,
                "name": self.name,
                }


class Categories(BaseDB):
    def __init__(self):
        super().__init__(Category)

    async def new(self, instance: Category):
        await self._add_obj(instance)

    async def get(self, id: int) -> Category | None:
        result = await self._get_object(id)
        return result

    async def update(self, instance: Category) -> None:
        await self._update_obj(instance=instance)

    async def delete(self, instance: Category) -> None:
        await self._delete_obj(instance=instance)

    async def in_(self, id: int) -> Category | bool:
        result = await self.get(id)
        if type(result) is Category:
            return result
        return False

    async def get_by_name(self, name):
        filters = {Category.name: name}
        result = await self._get_objects(filters)
        if result:
            return result[0]

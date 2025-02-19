import logging

from sqlalchemy import Column, String, Integer, ForeignKey

from .base import Base, BaseDB

logger = logging.getLogger(__name__)


class Subcategory(Base):
    __tablename__ = "subcategories"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"))

    refs = []

    def dict(self):
        return {"id": self.id,
                "name": self.name,
                "category_id": self.category_id,
                }


class Subcategories(BaseDB):
    def __init__(self):
        super().__init__(Subcategory)

    async def new(self, instance: Subcategory):
        await self._add_obj(instance)

    async def get(self, id: int) -> Subcategory | None:
        result = await self._get_object(id)
        return result

    async def update(self, instance: Subcategory) -> None:
        await self._update_obj(instance=instance)

    async def delete(self, instance: Subcategory) -> None:
        await self._delete_obj(instance=instance)

    async def in_(self, id: int) -> Subcategory | bool:
        result = await self.get(id)
        if type(result) is Subcategory:
            return result
        return False

    async def get_by_name(self, name):
        filters = {Subcategory.name: name}
        result = await self._get_objects(filters)
        if not result:
            return False
        return result[0]


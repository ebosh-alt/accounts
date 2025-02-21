import logging
from sqlalchemy import Column, String, Integer, select

from .base import Base, BaseDB

from internal.entities.database.subcategories import Subcategory
from internal.entities.database.accounts import Account


logger = logging.getLogger(__name__)


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)

    refs = []

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
    
    async def get_viewed_categories(self):
        # Запрос для получения категорий с хотя бы одним аккаунтом с view_type = True
        async with await self._get_session() as session:
            result = await session.execute(
                select(Category).distinct(
                    ).join(Subcategory, Subcategory.category_id == Category.id
                    ).join(Account, Account.subcategory_id == Subcategory.id
                    ).filter(Account.view_type == True)
            )

            categories_with_view_type_true = result.scalars().all()
        return [cat.name for cat in categories_with_view_type_true]


    async def get_viewed_subcategories_by_category(self, category):
        # Запрос для получения категорий с хотя бы одним аккаунтом с view_type = True
        async with await self._get_session() as session:
            result = await session.execute(
                select(Subcategory).distinct(
                    ).join(Category, Category.id == Subcategory.category_id
                    ).join(Account, Account.subcategory_id == Subcategory.id
                    ).filter(Account.view_type == True
                    ).filter(Category.name == category)
            )

            subcategories_with_view_type_by_category = result.scalars().all()
        return [sub.name for sub in subcategories_with_view_type_by_category]


    async def get_viewed_accs_by_category_subcategory(self, category, subcategory):
        # Запрос для получения категорий с хотя бы одним аккаунтом с view_type = True
        async with await self._get_session() as session:
            result = await session.execute(
                select(Account).distinct(
                    ).join(Subcategory, Account.subcategory_id == Subcategory.id
                    ).join(Category, Subcategory.category_id == Category.id
                    ).filter(Account.view_type == True
                    ).filter(Subcategory.name == subcategory
                    ).filter(Category.name == category
                )
            )

            accs_with_view_type_by_category_subcategory = result.scalars().all()
        return [acc.name for acc in accs_with_view_type_by_category_subcategory], accs_with_view_type_by_category_subcategory
        # return accs_with_view_type_by_category_subcategory

    async def get_viewed_accs_by_category_subcategory_acc(self, category, subcategory, acc):
        # Запрос для получения категорий с хотя бы одним аккаунтом с view_type = True
        async with await self._get_session() as session:
            result = await session.execute(
                select(Account).distinct(
                    ).join(Subcategory, Account.subcategory_id == Subcategory.id
                    ).join(Category, Category.id == Subcategory.category_id
                    ).filter(Account.view_type == True
                    ).filter(Category.name == category
                    ).filter(Subcategory.name == subcategory
                    ).filter(Account.name == acc)
            )

            accs_with_view_type_by_category_subcategory = result.scalars().all()
        # return [acc.name for acc in accs_with_view_type_by_category_subcategory]
        return accs_with_view_type_by_category_subcategory


    async def get_by_name(self, name):
        filters = {Category.name: name}
        result = await self._get_objects(filters)
        if not result:
            return False
        return result[0]

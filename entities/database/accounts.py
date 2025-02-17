import logging
from typing import Any

from sqlalchemy import Column, String, Boolean, FLOAT, Integer

from data.config import Config
from service.Excel.excel import get_account_data
from .base import Base, BaseDB
from ..models import Response
from ..schemas.Catalog import Catalog

logger = logging.getLogger(__name__)


class Account(Base):
    __tablename__ = "accounts"
    id: int = Column(Integer, autoincrement="auto", primary_key=True)
    shop: str = Column(String)
    price: float = Column(FLOAT)
    description: str = Column(String)
    data: str = Column(String)
    view_type: bool = Column(Boolean)
    name: str = Column(String)
    deal_id: int = Column(Integer)
    uid: str = Column(String, unique=True)

    def dict(self):
        return {
            "id": self.id,
            "shop": self.shop,
            "price": self.price,
            "description": self.description,
            "data": self.data,
            "view_type": self.view_type,
            "name": self.name,
            "deal_id": self.deal_id,
            "uid": self.uid,
        }


class Accounts(BaseDB):
    async def new(self, account: Account):
        await self._add_obj(account)

    async def get(self, id: int) -> Account | None:
        result = await self._get_object(Account, id)
        return result

    async def update(self, account: Account) -> None:
        await self._update_obj(instance=account, obj=Account)

    async def delete(self, account: Account) -> None:
        await self._delete_obj(instance=account)

    async def in_(self, id: int) -> Account | bool:
        result = await self.get(id)
        if result is Account:
            return result
        return False

    async def get_shops(self) -> list[Any]:
        filters = {Account.view_type: True}
        data = await self._get_objects(obj=Account, filters=filters)
        result = []
        [result.append(i.shop) for i in data if i.shop not in result]
        return result

    async def get_account_by_name(self, name, shop):
        filters = {Account.name: name, Account.shop: shop, Account.view_type: True}
        result: list[Account] = await self._get_objects(obj=Account, filters=filters)
        account = result
        return account

    async def get_name_accounts_shop(self, shop: str):
        filters = {Account.shop: shop, Account.view_type: True}
        request = await self._get_objects(obj=Account, filters=filters)
        result = []
        for i in request:
            if len(i.name) < 65 and i.name not in result:
                result.append(i.name)
        return result

    async def get_last(self) -> Account:
        filters = {}
        data = await self._get_objects(Account, filters)
        return data[-1]

    async def get_by_deal_id(self, deal_id) -> list[Account]:
        filters = {Account.deal_id: deal_id}
        result = await self._get_objects(Account, filters)
        return result

    async def in_uid(self, value) -> Account | bool:
        result = await self._in(Account, Account.uid, [value])
        if len(result) == 0:
            return False
        return result[0]

    async def replace_catalog(self, path) -> Response:
        """
        Замена всего каталога
        """
        accounts_mds = get_account_data(path)
        accounts = []
        er = False
        config = Config()
        for account_md in accounts_mds:
            logger.info(await self.in_uid(account_md.uid) is False)
            if await self.in_uid(account_md.uid) is False:
                if account_md.type_account in config.acceptable_account_types:
                    accounts.append(Account(
                        shop=account_md.type_account,
                        price=account_md.price,
                        description=account_md.description,
                        data=account_md.data,
                        view_type=True,
                        name=account_md.name,
                        uid=account_md.uid
                    ))
                else:
                    return Response(status=402, description="the account type is not allowed")
            else:
                er = True
        if er:
            return Response(status=403, description="uid in db")
        await self._update_all_values(Account, Account.view_type, False)
        er = not await self._bulk_add(accounts)
        if er:
            return Response(status=404, description="new accounts empty")
        else:
            return Response(status=200, description="success replace catalog")

    async def change_catalog(self, path) -> Response:
        """
        Изменение каталога
        """
        account: Account
        accounts_mds = get_account_data(path)
        config = Config()
        for account_md in accounts_mds:
            if account := await self.in_uid(account_md.uid):
                if not account.deal_id:
                    if account_md.type_account in config.acceptable_account_types:
                        account.shop = account_md.type_account
                        account.price = account_md.price
                        account.description = account_md.description
                        account.data = account_md.data
                        account.view_type = True
                        account.name = account_md.name
                        account.uid = account_md.uid
                        await self.update(account)
                    else:
                        return Response(status=403, description="the account type is not allowed")
                else:
                    return Response(status=404, description="deal has been created for the account")
        return Response(status=200, description="success change catalog")

    async def delete_from_catalog(self, path) -> Response:
        """
        Удаление из каталога
        """
        accounts_mds = get_account_data(path)
        accounts = []
        for account_md in accounts_mds:
            if account := await self.in_uid(account_md.uid):
                account.view_type = False
                accounts.append(account)
            else:
                return Response(status=403, description="uid not in db")
        er = not await self._bulk_add(accounts)
        if er:
            return Response(status=404, description="new accounts empty")
        else:
            return Response(status=200, description="success delete from catalog")

    async def get_unique_accounts_with_count(self) -> Catalog:
        """
        Получить список уникальных аккаунтов с view_type=True,
        сгруппированных по (shop, name), а также количество
        аккаунтов для каждой группы.
        """
        # Фильтр для выборки только активных аккаунтов
        filters = {Account.view_type: True}
        accounts = await self._get_objects(Account, filters=filters)

        # Словарь для группировки аккаунтов
        grouped_accounts = {}
        for account in accounts:
            key = (account.shop, account.name)  # Уникальный ключ: (shop, name)
            if key not in grouped_accounts:
                grouped_accounts[key] = {
                    "category": account.shop,
                    "name": account.name,
                    "description": account.description,
                    "price": account.price,
                    "uid": account.uid,
                    "count": 0,
                }

            grouped_accounts[key]["count"] += 1

        data = {"accounts": list(grouped_accounts.values())}
        logger.info(data)
        catalog = Catalog(**data)
        return catalog

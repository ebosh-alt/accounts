import logging
import math

import pandas as pd

from internal.entities.database import (
    acceptable_account_categories, subcategories, categories, Category, Account, Subcategory, accounts
)
from internal.entities.models import AccountExcel, Response

logger = logging.getLogger(__name__)


class Excel:
    columns_name = {
        "Категория": "category",
        "Подкатегория": "subcategory",
        "Название": "name",
        "Стоимость": "price",
        "Описание": "description",
        "Данные": "data",
        "UID": "uid"
    }
    current_general_data = {
        "category": None,
        "subcategory": None,
        "name": None,
        "price": None,
        "description": None,
        "data": None,
        "uid": None
    }
    @classmethod
    async def replace_catalog(cls, file_path) -> Response:
        """
        Замена всего каталога
        """
        instances_mds: list[AccountExcel] = cls.get_account_data(file_path)
        instances: list = []
        er = False

        # TODO: add acceptable_types_names
        acceptable_types_names = await acceptable_account_categories.get(1)

        for instance_md in instances_mds:
            account = await accounts.get_by_uid(instance_md.uid)

            if account is False:
                if instance_md.category:
                    subcategory = await subcategories.get_by_name(instance_md.subcategory)
                    category = await categories.get_by_name(instance_md.category)

                    if category is False:
                        category = Category()
                        category.name = instance_md.category
                        await categories.new(category)

                    if subcategory is False:
                        subcategory = Subcategory()
                        subcategory.name = instance_md.subcategory
                        subcategory.category_id = category.id
                        await subcategories.new(subcategory)

                    instances.append(Account(
                        subcategory_id=subcategory.id,
                        price=instance_md.price,
                        description=instance_md.description,
                        data=instance_md.data,
                        view_type=True,
                        name=instance_md.name,
                        uid=instance_md.uid
                    ))
                else:
                    return Response(status=402, description="the instance type is not allowed")
            else:
                er = True
        if er:
            return Response(status=403, description="uid in db")

        await accounts._update_all_values(Account.view_type, False)
        er = not await accounts._bulk_add(instances)
        if er:
            return Response(status=404, description="new instances empty")
        else:

            return Response(status=200, description="success replace catalog")

    @classmethod
    async def change_catalog(cls, file_path) -> Response:
        """
        Изменение каталога
        """
        instance: Account
        instances_mds: list[AccountExcel] = cls.get_account_data(file_path)
        acceptable_types_category = await acceptable_account_categories.get_all_name_types()
        for instance_md in instances_mds:
            account = await accounts.get_by_uid(instance_md.uid)
            if type(account) is Account:
                if not account.deal_id:
                    if instance_md.category:
                        subcategory = await subcategories.get(account.subcategory_id)
                        category = await categories.get(subcategory.category_id)

                        subcategory.name = instance_md.subcategory
                        category.name = instance_md.category

                        await categories.update(category)
                        await subcategories.update(subcategory)

                        account.category_id = category.id
                        account.price = instance_md.price
                        account.description = instance_md.description
                        account.data = instance_md.data
                        account.view_type = True
                        account.name = instance_md.name
                        account.uid = instance_md.uid
                        await accounts.update(account)
                    else:
                        return Response(status=403, description="the instance type is not allowed")
                else:
                    return Response(status=404, description="deal has been created for the instance")
        return Response(status=200, description="success change catalog")

    @classmethod
    async def delete_from_catalog(cls, file_path) -> Response:
        """
        Удаление из каталога
        """
        instances_mds = cls.get_account_data(file_path)
        instances = []
        for instance_md in instances_mds:
            if instance := await accounts.in_uid(instance_md.uid):
                instance.view_type = False
                instances.append(instance)
            else:
                return Response(status=403, description="uid not in db")
        er = not await accounts._bulk_add(instances)
        if er:
            return Response(status=404, description="new instances empty")
        else:
            return Response(status=200, description="success delete from catalog")

    @classmethod
    def get_excel_dict(cls, file_path) -> dict[str: list[str]]:
        xl = pd.ExcelFile(file_path)
        df1 = xl.parse(xl.sheet_names[0])
        data = {}

        for column_name in df1.columns:
            column_ = df1[column_name]
            new_acc = []
            for cell_ in column_:
                new_acc.append(cell_)
            data[cls.columns_name[column_name]] = new_acc
        return data

    @classmethod
    def get_account_data(cls, file_path: str) -> list[AccountExcel]:
        accounts_data = []

        # Загружаем данные из файла
        data = cls.get_excel_dict(file_path)
        # Инициализируем текущие общие данные

        # Основной цикл
        for i in range(len(data.get("category", []))):
            # Обновляем общие данные, если они указаны в текущей строке
            for key in cls.current_general_data.keys():
                if key in data and i < len(data[key]) and (
                        isinstance(data[key][i], str) or not math.isnan(data[key][i])
                ):
                    cls.current_general_data[key] = data[key][i]

            # Проверяем наличие уникальных данных
            if not all(
                    (key not in data or i >= len(data[key]) or math.isnan(data[key][i]))
                    if key in data and i < len(data[key]) and isinstance(data[key][i], float) else False
                    for key in ["data", "uid"]
            ):
                account = {
                    "category": str(cls.current_general_data["category"]),
                    "subcategory": str(cls.current_general_data["subcategory"]),
                    "name": cls.current_general_data["name"],
                    "price": cls.current_general_data["price"],
                    "description": str(cls.current_general_data["description"]),
                    "data": data.get("data", [None])[i]
                    if i < len(data.get("data", [])) and not (
                            isinstance(data["data"][i], float) and math.isnan(data["data"][i])
                    )
                    else None,
                    "uid": str(data["uid"][i])
                    if "uid" in data and i < len(data["uid"]) and not (
                            isinstance(data["uid"][i], float) and math.isnan(data["uid"][i])
                    )
                    else None,
                }
                accounts_data.append(AccountExcel(**account))

        return accounts_data

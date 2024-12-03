import json
import math

import pandas as pd

from models.models import AccountExcel

# from models.database import accounts, Account
columns_name = {
    "Тип аккаунта": "type_account",
    "Стоимость аккаунта": "price",
    "Описание  аккаунта": "description",
    "Данные аккаунта": "data",
    "Название": "name",
    "UIID": "uid"
}


def get_excel_dict(file_name) -> dict[str: list[str]]:
    xl = pd.ExcelFile(file_name)
    df1 = xl.parse(xl.sheet_names[0])
    data = {}

    for column_name in df1.columns:
        column_ = df1[column_name]
        new_acc = []
        for cell_ in column_:
            new_acc.append(cell_)
        data[columns_name[column_name]] = new_acc
    return data


# async def create_accounts(file_name):
#     data = get_excel_dict(file_name)
#     for i in range(len(data["Магазин"])):
#         acc = Account(
#             shop=data["Магазин"][i],
#             price=data["Стоимость"][i],
#             description=data["Описание проекта"][i],
#             data=data["Данные"][i],
#             view_type=True,
#             name=data["name"][i]
#         )
#         await accounts.new(acc)


def parse_account_data(file_path: str):
    accounts = []
    data = get_excel_dict(file_path)
    current_general_data = {
        "type_account": None,
        "name": None,
        "price": None,
        "description": None
    }

    for i in range(len(data["type_account"])):
        # Обновляем общие данные, если они есть
        for key in current_general_data.keys():
            if isinstance(data[key][i], str) or not math.isnan(data[key][i]):
                current_general_data[key] = data[key][i]

        # Если есть уникальные данные, добавляем их с дублированием общих данных
        if not all(math.isnan(data[key][i]) if isinstance(data[key][i], float) else False for key in
                   ["data", "uid"]):
            account = {
                "type_account": current_general_data["type_account"],
                "name": current_general_data["name"],
                "price": current_general_data["price"],
                "description": current_general_data["description"],
                "data": data["data"][i] if not (
                        isinstance(data["data"][i], float) and math.isnan(data["data"][i])) else None,
                "uid": int(data["uid"][i]) if not (
                        isinstance(data["uid"][i], float) and math.isnan(data["uid"][i])) else None,
            }
            accounts.append(AccountExcel(**account))
    return accounts


def get_data(file_path):
    data = get_excel_dict(file_path)


if __name__ == '__main__':
    # Run the function on the uploaded file
    account_data = parse_account_data(r"D:\tg_bots\accounts\service\Excel\template_new.xlsx")
    print(json.dumps(account_data, indent=4, ensure_ascii=False))
    # for i in account_data:
    #     print(len(account_data[i]))

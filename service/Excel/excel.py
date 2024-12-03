import json
import math

import pandas as pd

from models.models import AccountExcel

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


def get_account_data(file_path: str) -> list[AccountExcel]:
    accounts = []

    # Загружаем данные из файла
    data = get_excel_dict(file_path)
    print(data)
    # Инициализируем текущие общие данные
    current_general_data = {
        "type_account": None,
        "name": None,
        "price": None,
        "description": None
    }

    # Основной цикл
    for i in range(len(data.get("type_account", []))):
        # Обновляем общие данные, если они указаны в текущей строке
        for key in current_general_data.keys():
            if key in data and i < len(data[key]) and (
                    isinstance(data[key][i], str) or not math.isnan(data[key][i])
            ):
                current_general_data[key] = data[key][i]

        # Проверяем наличие уникальных данных
        if not all(
                (key not in data or i >= len(data[key]) or math.isnan(data[key][i]))
                if key in data and i < len(data[key]) and isinstance(data[key][i], float) else False
                for key in ["data", "uid"]
        ):
            account = {
                "type_account": current_general_data["type_account"],
                "name": current_general_data["name"],
                "price": current_general_data["price"],
                "description": current_general_data["description"],
                "data": data.get("data", [None])[i]
                if i < len(data.get("data", [])) and not (
                        isinstance(data["data"][i], float) and math.isnan(data["data"][i])
                )
                else None,
                "uid": int(data["uid"][i])
                if "uid" in data and i < len(data["uid"]) and not (
                        isinstance(data["uid"][i], float) and math.isnan(data["uid"][i])
                )
                else None,
            }
            accounts.append(AccountExcel(**account))

    return accounts


if __name__ == '__main__':
    # Run the function on the uploaded file
    account_data = get_account_data(r"D:\tg_bots\accounts\service\Excel\template_del.xlsx")

    # for i in account_data:
    #     print(len(account_data[i]))

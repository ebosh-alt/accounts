import pandas as pd
from models.database import accounts, Account


def get_excel_dict(file_name) -> dict[str: list[str]]:
    xl = pd.ExcelFile(file_name)
    df1 = xl.parse(xl.sheet_names[0])
    data = {}
    for column_name in df1.columns:
        column_ = df1[column_name]
        new_acc = []
        for cell_ in column_:
            new_acc.append(cell_)
        data[column_name] = new_acc
    return data


async def create_accounts(file_name):
    data = get_excel_dict(file_name)
    for i in range(len(data["Shop"])):
        acc = Account(
            shop = data["Shop"][i],
            price = data["Price"][i],
            description = data["Description"][i],
            data = data["Data"][i],
            view_type = True,
            name = data["Name"][i]
        )
        await accounts.new(acc)


# if __name__ == "__main__":
#     create_accounts(file_name='./service/ExcelS/Template.xlsx')
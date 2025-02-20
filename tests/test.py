from config.config import config

from internal.entities.database import sellers, Seller, users, User, accounts, Account, deals, Deal, subcategories, Subcategory, categories, Category, shops, Shop

import datetime


async def create_test_data():


    # Добавление записей в таблицу categories
    for i in range(1, 11):
        category = Category(
            id=i,
            name=f"Category Name {i}",
        )
        await categories.new(category)

    # Добавление записей в таблицу subcategories
    for i in range(1, 11):
        subcategory = Subcategory(
            id=i,
            name=f"Subcategory Name {i}",
            category_id=i,
        )
        await subcategories.new(subcategory)

    # Добавление записей в таблицу deals
    for i in range(1, 5):
        deal = Deal(
            buyer_id=config.manager.seller_id,
            seller_id=config.manager.seller_id,
            price=100.0 + i,
            wallet=f"wallet_{i}",
            date=datetime.datetime.now(),
            guarantor=bool(i % 2),
            payment_status=0
        )
        await deals.new(deal)

    # Добавление записей в таблицу accounts
    for i in range(1, 11):
        account = Account(
            subcategory_id=i,
            price=100.0 + i,
            description=f"Description {i}",
            data=f"Data {i}",
            view_type=bool(i % 2),
            name=f"Account {i}",
            uid=str(i),
            deal_id=i % 4 + 1
        )
        await accounts.new(account)
    
    for i in range(11, 21):
        account = Account(
            subcategory_id=5,
            price=100.0 + i,
            description=f"Description {i}",
            data=f"Data {i}",
            view_type=True,
            name=f"Account {i}",
            uid=str(i),
            deal_id=None
        )
        await accounts.new(account)



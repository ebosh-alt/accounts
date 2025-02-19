from config.config import config

from internal.entities.database import sellers, Seller, users, User, accounts, Account, deals, Deal, subcategories, Subcategory, categories, Category

import datetime

async def create_seller():
    if await sellers.in_(id=config.manager.seller_id):
        pass
    else:
        seller = Seller(id=config.manager.seller_id, rating=5, balance=0, username=config.manager.username, wallet="wallet")
        await sellers.new(seller=seller)

    # Добавление записей в таблицу users
    if await users.in_(id=config.manager.seller_id):
        pass
    else:
        user = User(id=config.manager.seller_id, username=config.manager.username)
        await users.new(user)

async def create_test_data():
    # Добавление записи в таблицу sellers
    if await sellers.in_(id=config.manager.seller_id):
        pass
    else:
        seller = Seller(id=config.manager.seller_id, rating=5, balance=0, username=config.manager.username, wallet="wallet")
        await sellers.new(seller=seller)

    # Добавление записей в таблицу users
    if await users.in_(id=config.manager.seller_id):
        pass
    else:
        user = User(id=config.manager.seller_id, username=config.manager.username)
        await users.new(user)

    # Добавление записей в таблицу categories
    for i in range(1, 11):
        category = Category(
            id=i,
            name=f"Name{i}",
        )
        await categories.new(category)

    # Добавление записей в таблицу subcategories
    for i in range(1, 11):
        subcategory = Subcategory(
            id=i,
            name=f"Name{i}",
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



from config.config import config

from internal.entities.database import sellers, Seller, users, User, accounts, Account, deals, Deal

import datetime


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
        await users.new(user=user)

    # Добавление записей в таблицу accounts
    for i in range(1, 11):
        account = Account(
            shop=f"shop_{i}",
            price=100.0 + i,
            description=f"Description {i}",
            data=f"Data {i}",
            view_type=bool(i % 2),
            name=f"Account {i}",
            uid=str(i),
            # deal_id=i % 4 + 1
        )
        await accounts.new(account)

    # Добавление записей в таблицу deals
    for i in range(1, 5):
        deal = Deal(
            buyer_id=i,
            seller_id=config.manager.seller_id,
            price=100.0 + i,
            wallet=f"wallet_{i}",
            date=datetime.datetime.now(),
            guarantor=bool(i % 2),
            payment_status=0
        )
        await deals.new(deal)


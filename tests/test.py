import datetime

from models.database import accounts, Account, users, Chat, chats, Seller, sellers, deals, Deal, User
from data.config import SELLER, USERNAME


async def new_data():
    await accounts.new(
        Account(id=0, shop="Goggle", price=100.0, description="description1", data=datetime.datetime.now(),
                view_type=True,
                name="name1"))
    await accounts.new(
        Account(shop="Facebook", price=110.0, description="description2", data=datetime.datetime.now(), view_type=True,
                name="name2"))
    await accounts.new(
        Account(shop="Amazon", price=120.0, description="description3", data=datetime.datetime.now(), view_type=True,
                name="name3"))
    await accounts.new(
        Account(shop="Apple", price=130.0, description="description4", data=datetime.datetime.now(), view_type=True,
                name="name4"))
    await accounts.new(
        Account(shop="Uber", price=140.0, description="description5", data=datetime.datetime.now(), view_type=True,
                name="name5"))
    await accounts.new(
        Account(shop="Goggle", price=150.0, description="description6", data=datetime.datetime.now(), view_type=True,
                name="name6"))
    await users.new(User(id=1, username="username1"))
    await users.new(User(id=2, username="username2"))
    await users.new(User(id=3, username="username3"))
    # await sellers.new(Seller(id=SELLER, rating=0, balance=0, username=USERNAME))
    await chats.new(Chat(id=1, user_id=1, seller_id=1))
    await chats.new(Chat(id=2, user_id=2, seller_id=1))
    await chats.new(Chat(id=3, user_id=3, seller_id=1))
    await deals.new(
        Deal(buyer_id=6989531851, seller_id=1, account_id=1,
             date=datetime.datetime.now() - datetime.timedelta(hours=10), guarantor=False, payment_status=1))
    await deals.new(
        Deal(buyer_id=6989531851, seller_id=1, account_id=2, date=datetime.datetime.now() - datetime.timedelta(hours=2),
             guarantor=False, payment_status=1))
    await deals.new(
        Deal(buyer_id=6989531851, seller_id=1, account_id=3,
             date=datetime.datetime.now() - datetime.timedelta(hours=18), guarantor=False, payment_status=1))

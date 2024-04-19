from datetime import datetime

from models.database import accounts, Account, User, users, Chat, chats, Seller, sellers, deals, Deal


async def new_data():
    await accounts.new(Account(shop="Goggle", price=100.0, description="description1", data=datetime.now(), view_type=True,
                         name="name1"))
    await accounts.new(Account(shop="Facebook", price=110.0, description="description2", data=datetime.now(), view_type=True,
                         name="name2"))
    await accounts.new(Account(shop="Amazon", price=120.0, description="description3", data=datetime.now(), view_type=True,
                         name="name3"))
    await accounts.new(Account(shop="Apple", price=130.0, description="description4", data=datetime.now(), view_type=True,
                         name="name4"))
    await accounts.new(Account(shop="Uber", price=140.0, description="description5", data=datetime.now(), view_type=True,
                         name="name5"))
    await accounts.new(Account(shop="Goggle", price=150.0, description="description6", data=datetime.now(), view_type=True,
                         name="name6"))
    await users.new(User(id=1, username="username1"))
    await users.new(User(id=2, username="username2"))
    await users.new(User(id=3, username="username3"))
    await sellers.new(Seller(id=1, rating=4, balance=4, username="username4"))
    await sellers.new(Seller(id=2, rating=5, balance=5, username="username5"))
    await sellers.new(Seller(id=3, rating=6, balance=6, username="username6"))
    await chats.new(Chat(id=1, user_id=1, seller_id=1))
    await chats.new(Chat(id=2, user_id=2, seller_id=1))
    await chats.new(Chat(id=3, user_id=3, seller_id=1))
    await deals.new(Deal(buyer_id=1, seller_id=1, account_id=1, date=datetime.now(), guarantor=False, payment_status=1))
    await deals.new(Deal(buyer_id=1, seller_id=1, account_id=2, date=datetime.now(), guarantor=False, payment_status=1))
    await deals.new(Deal(buyer_id=1, seller_id=1, account_id=0, date=datetime.now(), guarantor=False, payment_status=1))
    await deals.new(Deal(buyer_id=2, seller_id=3, account_id=0, date=datetime.now(), guarantor=False, payment_status=1))
    await deals.new(Deal(buyer_id=2, seller_id=2, account_id=2, date=datetime.now(), guarantor=False, payment_status=1))
    await deals.new(Deal(buyer_id=3, seller_id=3, account_id=1, date=datetime.now(), guarantor=False, payment_status=1))

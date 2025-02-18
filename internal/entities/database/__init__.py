from .deals import Deal, Deals
from .chats import Chat, Chats
from .users import User, Users
from .sellers import Seller, Sellers
from .accounts import Account, Accounts

users: Users = Users()
sellers: Sellers = Sellers()
deals: Deals = Deals()
accounts: Accounts = Accounts()
chats: Chats = Chats()
__al__ = ("Deal", "deals", "Chat", "chats", "User", "users", "Seller", "sellers", "Account", "accounts")

from internal.entities.database.acceptable_account_categories import AcceptableAccountCategory, AcceptableAccountCategories
from internal.entities.database.accounts import Account, Accounts
from internal.entities.database.categories import Category, Categories
from internal.entities.database.chats import Chat, Chats
from internal.entities.database.deals import Deal, Deals
from internal.entities.database.sellers import Seller, Sellers
from internal.entities.database.shops import Shop, Shops
from internal.entities.database.subcategories import Subcategory, Subcategories
from internal.entities.database.users import User, Users

users: Users = Users()
sellers: Sellers = Sellers()
deals: Deals = Deals()
accounts: Accounts = Accounts()
chats: Chats = Chats()
shops: Shops = Shops()
categories: Categories = Categories()
subcategories: Subcategories = Subcategories()
acceptable_account_categories: AcceptableAccountCategories = AcceptableAccountCategories()

__all__ = ("Deal", "deals",
           "Chat", "chats",
           "User", "users",
           "Seller", "sellers",
           "Account", "accounts",
           "Category", "categories",
           "Subcategory", "subcategories",
           "Shop", "shops",
           "AcceptableAccountCategory", "acceptable_account_categories",
           )

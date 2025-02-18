from .acceptable_account_categories import AcceptableAccountCategory, AcceptableAccountCategories
from .accounts import Account, Accounts
from .categories import Category, Categories
from .chats import Chat, Chats
from .deals import Deal, Deals
from .sellers import Seller, Sellers
from .shops import Shop, Shops
from .subcategories import Subcategory, Subcategories
from .users import User, Users

users: Users = Users()
sellers: Sellers = Sellers()
deals: Deals = Deals()
accounts: Accounts = Accounts()
chats: Chats = Chats()
shops: Shops = Shops()
categories: Categories = Categories()
subcategories: Subcategories = Subcategories()
acceptable_account_categories: AcceptableAccountCategories = AcceptableAccountCategories()

__al__ = ("Deal", "deals",
          "Chat", "chats",
          "User", "users",
          "Seller", "sellers",
          "Account", "accounts",
          "Category", "categories",
          "Subcategory", "subcategories",
          "Shop", "shops",
          "AcceptableAccountCategory", "acceptable_account_categories"
          )

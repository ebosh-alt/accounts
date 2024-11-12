from aiogram.fsm.state import StatesGroup, State


class UserStates(StatesGroup):
    ShoppingCart = State()
    MailingSeller = State()
    Manually = State()


class AdminStates(StatesGroup):
    enter_buyer_wallet = State()
    change_seller_wallet = State()
    cancel_buy = State()
    change_balance = State()
    change_about_shop = State()


class ManagerStates(StatesGroup):
    change_wallet = State()
    get_excel_file = State()
    create_deal_user_id = State()
    create_deal_shop = State()
    create_deal_price = State()
    create_deal_description = State()
    create_deal_data = State()
    create_deal_name = State()
    create_deal_guarant = State()
    create_deal_end = State()



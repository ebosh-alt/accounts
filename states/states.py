from aiogram.fsm.state import StatesGroup, State


class UserStates(StatesGroup):
    ShoppingCart = State()
    MailingSeller = State()
    Manually = State()


class AdminStates(StatesGroup):
    cancel_buy = State()
    change_balance = State()


class ManagerStates(StatesGroup):
    get_excel_file = State()
    create_deal_user_id = State()
    create_deal_shop = State()
    create_deal_price = State()
    create_deal_description = State()
    create_deal_data = State()
    create_deal_name = State()
    create_deal_guarant = State()
    create_deal_end = State()



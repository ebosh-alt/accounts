from aiogram.fsm.state import StatesGroup, State


class UserStates(StatesGroup):
    ShoppingCart = State()


class AdminStates(StatesGroup):
    cancel_buy = State()


class ManageStates(StatesGroup):
    ...

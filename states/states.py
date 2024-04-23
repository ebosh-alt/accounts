from aiogram.fsm.state import StatesGroup, State


class UserStates(StatesGroup):
    basket = State()


class AdminStates(StatesGroup):
    cancel_buy = State()


class ManageStates(StatesGroup):
    ...

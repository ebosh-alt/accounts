from aiogram.fsm.state import StatesGroup, State


class UserStates(StatesGroup):
    ...


class AdminStates(StatesGroup):
    cancel_buy = State()


class ManageStates(StatesGroup):
    ...

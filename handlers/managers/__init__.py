# from .start import start_rt
# from .admin import admin_rt
from .menu import manager_rt
from .accounts import accounts_rt
from .deals import deals_rt
from .communication import communication_rt
from .wallet import wallet_rt


manager_routers = (manager_rt, accounts_rt, deals_rt, communication_rt, wallet_rt,)

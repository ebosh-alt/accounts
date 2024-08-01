from .view_history import history_buy_rt
from .menu import menu_rt
from .buy_automatically import buy_automatically_rt
from .buy_manually import buy_manually_rt
from .product_evaluation import product_evaluation_rt

users_routers = (menu_rt, buy_automatically_rt, history_buy_rt, buy_manually_rt, product_evaluation_rt)

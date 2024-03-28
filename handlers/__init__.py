from .start import start_rt
from .admin import routers
routers = (*routers, start_rt, )

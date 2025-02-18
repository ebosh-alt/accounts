from .admins import admin_routers
from .managers import manager_routers
from .users import users_routers

routers = (*admin_routers, *users_routers, *manager_routers)



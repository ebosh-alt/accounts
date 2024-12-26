from fastapi import APIRouter

from .v1.endpoints.catalog import router as router_catalog

routers = APIRouter()

routers.include_router(router_catalog)

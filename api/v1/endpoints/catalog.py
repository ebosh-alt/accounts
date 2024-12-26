from fastapi import APIRouter

from models.database import accounts
from models.schemas.Catalog import Response
from service.FastApi.services.Create import logger

router = APIRouter(prefix='/api/catalog', tags=['Каталог'])


@router.get("/getCatalog", summary="Получение каталога")
async def get_catalog():
    catalog = await accounts.get_unique_accounts_with_count()
    logger.info(catalog)
    return Response(**{"status_code": 200, "message": {"accounts": catalog.accounts, "status": "success"}})

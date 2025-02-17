from fastapi import APIRouter

from entities.database import accounts
from entities.schemas.Catalog import Response

router = APIRouter(prefix='/api/catalog', tags=['Каталог'])


@router.get("/getCatalog", summary="Получение каталога")
async def get_catalog():
    try:
        catalog = await accounts.get_unique_accounts_with_count()
        return Response(
            **{"message": {"catalog": catalog.accounts, "status": "success", "detail": "Complete get catalog"}})
    except Exception as e:
        return Response(**{"message": {"catalog": [], "status": "error", "detail": e}})

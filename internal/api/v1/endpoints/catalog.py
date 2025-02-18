from fastapi import APIRouter

from internal.entities.database import accounts
from internal.entities.schemas.Catalog import Response

### TODO: edit logic 

router = APIRouter(prefix='/api/catalog', tags=['Каталог'])


@router.get("/getCatalog", summary="Получение каталога")
async def get_catalog():
    try:
        catalog = await accounts.get_unique_accounts_with_count()
        return Response(
            **{"message": {"catalog": catalog.accounts, "status": "success", "detail": "Complete get catalog"}})
    except Exception as e:
        return Response(**{"message": {"catalog": [], "status": "error", "detail": e}})

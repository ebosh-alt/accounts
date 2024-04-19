from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from data.config import SQLALCHEMY_DATABASE_URI

Base = declarative_base()

__factory = None


async def create_async_database():
    global __factory
    engine = create_async_engine(SQLALCHEMY_DATABASE_URI)
    if __factory:
        return
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await create_session()
    await conn.close()


async def create_session():
    global __factory
    engine = create_async_engine(SQLALCHEMY_DATABASE_URI)
    __factory = sessionmaker(bind=engine, expire_on_commit=True, class_=AsyncSession)


def create_session_():
    global __factory
    return __factory()


class BaseDB:
    @staticmethod  # __table__ = "accounts"
    async def _get_session() -> AsyncSession:
        async with create_session_() as session:
            return session

    async def _add_obj(self, obj):
        async with await self._get_session() as session:
            session.add(obj)
            await session.commit()

    async def _get_obj(self, obj, id):
        async with await self._get_session() as session:
            res = await session.get(obj, id)
            return res

    async def _update_obj(self, obj, instance):
        async with await self._get_session() as session:
            query = update(obj).where(obj.id == instance.id).values(**instance.dict())
            await session.execute(query)
            await session.commit()

    async def _delete_obj(self, instance):
        async with await self._get_session() as session:
            await session.delete(instance)
            await session.commit()

    async def _get_attribute(self, obj, attribute: str):
        async with await self._get_session() as session:
            sql = update(obj).values(attribute)
            await session.execute(sql)
            await session.commit()

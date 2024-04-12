from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from data.config import SQLALCHEMY_DATABASE_URI

Base = declarative_base()


async def create_async_database():
    engine = create_async_engine(SQLALCHEMY_DATABASE_URI)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await conn.close()


class BaseDB:
    @staticmethod  # __table__ = "accounts"
    async def get_session() -> AsyncSession:
        engine = create_async_engine(SQLALCHEMY_DATABASE_URI)
        session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
        async with session() as ses:
            return ses

    async def add_obj(self, obj):
        async with await self.get_session() as session:
            session.add(obj)
            await session.commit()

    async def get_obj(self, obj, id):
        async with await self.get_session() as session:
            res = await session.get(obj, id)
            print(res)
            # sql = select(obj).where(obj.id == id)
            # query = await session.execute(sql)
            # user = query.scalar_one_or_none()
            return res

    async def update_obj(self, obj, instance):
        async with await self.get_session() as session:
            query = update(obj).where(obj.id == instance.id).values(**instance.dict())
            await session.execute(query)
            await session.commit()

    async def delete_obj(self, instance):
        async with await self.get_session() as session:
            await session.delete(instance)
            await session.commit()

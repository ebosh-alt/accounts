from functools import wraps
from os import environ
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import sqlalchemy.ext.declarative as dec
from sqlalchemy.orm import sessionmaker

# from sqlalchemy.dialects

# from .config import postgres
SqlAlchemyBase = dec.declarative_base()

env = environ.get

__factory = None


def get_database_url() -> str:
    return f'sqlite+aiosqlite:///data/database.db'


async def global_init():
    global __factory

    if __factory:
        return
    conn_str = get_database_url()

    engine = create_async_engine(conn_str)  # , pool_pre_ping=True, pool_size=50, max_overflow=10)

    async with engine.begin() as conn:
        await conn.run_sync(SqlAlchemyBase.metadata.create_all)

    __factory = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


def create_session() -> AsyncSession:
    global __factory
    return __factory()


def session_db(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with create_session() as session:
            return await func(*args, session=session, **kwargs)
    return wrapper

from sqlalchemy import Column, String, Boolean, BigInteger, FLOAT
from sqlalchemy.ext.asyncio import AsyncSession
from .base import Base


class User:
    id: int = Column(BigInteger, primary_key=True, autoincrement=True)
    shop: str = Column(String)
    price: float = Column(FLOAT)
    description: str = Column(String)
    data: str = Column(String)
    view_type: bool = Column(Boolean)
    name: str = Column(String)


class Users(Base):
    __tablename__ = "accounts"

    def __init__(self, session=AsyncSession):
        self.session = session

    def new(self, user: User):
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

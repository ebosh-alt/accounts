from sqlalchemy import Column, BigInteger, String, INTEGER, FLOAT, ForeignKey, select, delete, Boolean, update
from models.db import SqlAlchemyBase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

print("3456789")
class Chats(SqlAlchemyBase):
    __tablename__ = "chats"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    seller_id = Column(BigInteger, ForeignKey("sellers.id"))
    user = relationship("Users", back_populates="chats")
    seller = relationship("Sellers", back_populates="chats")

   
    @classmethod
    async def register(cls, id: int, user_id: int, seller_id: int, session: AsyncSession) -> None:
        if await cls.is_register(id, session):
            return
        sobj = cls(id=id, user_id=user_id, seller_id=seller_id)
        session.add(sobj)
        await session.commit()

    @classmethod
    async def obj(cls, id: int, session: AsyncSession):
        if not session.is_active:
            try:
                await session.begin()
            except Exception as e:
                print(e)
        _ = await session.execute(select(cls).where(cls.id == id))
        return _.scalar()
    
    @classmethod
    async def delete(cls, id: int, session: AsyncSession) -> None:
        if not session.is_active:
            try:
                await session.begin()
            except Exception as e:
                print(e)
        stmt = delete(cls).where(cls.id == id)
        await session.execute(stmt)
        await session.commit()

    @classmethod
    async def is_register(cls, id: int, session: AsyncSession) -> bool:
        if not session.is_active:
            try:
                await session.begin()
            except Exception as e:
                print(e)
        result = await session.execute(select(cls).filter_by(id=id))
        sobj = result.first()
        if sobj:
            return True
        else:
            return False


    # obj = get
    # delete
    # register
    # __contains__ = is_register
    

class Users(SqlAlchemyBase):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    username = Column(String)
    chats = relationship("Chats", back_populates="user", lazy="selectin")
    deals = relationship("Deals", back_populates="buyer", lazy="selectin")

   
    @classmethod
    async def register(cls, id: int, username: str, session: AsyncSession) -> None:
        if await cls.is_register(id, session):
            return
        sobj = cls(id=id, username=username)
        session.add(sobj)
        await session.commit()

    @classmethod
    async def obj(cls, id: int, session: AsyncSession):
        if not session.is_active:
            try:
                await session.begin()
            except Exception as e:
                print(e)
        _ = await session.execute(select(cls).where(cls.id == id))
        return _.scalar()
    
    @classmethod
    async def delete(cls, id: int, session: AsyncSession) -> None:
        if not session.is_active:
            try:
                await session.begin()
            except Exception as e:
                print(e)
        stmt = delete(cls).where(cls.id == id)
        await session.execute(stmt)
        await session.commit()

    @classmethod
    async def is_register(cls, id: int, session: AsyncSession) -> bool:
        if not session.is_active:
            try:
                await session.begin()
            except Exception as e:
                print(e)
        result = await session.execute(select(cls).filter_by(id=id))
        sobj = result.first()
        if sobj:
            return True
        else:
            return False
        
    @classmethod
    async def get_all(cls, session: AsyncSession) -> list:
        if not session.is_active:
            try:
                await session.begin()
            except Exception as e:
                print(e)

        result = await session.execute(select(cls))
        sobjs = result.scalars().all()

        return sobjs

    # obj = get +
    # delete +
    # register +
    # __contains__ = is_register +
    # get_all +

    

class Sellers(SqlAlchemyBase):
    __tablename__ = "sellers"

    id = Column(BigInteger, primary_key=True)
    rating = Column(BigInteger)
    balance = Column(BigInteger)
    username = Column(String)
    chats = relationship("Chats", back_populates="seller", lazy="selectin")
    deals = relationship("Deals", back_populates="seller", lazy="selectin")

   
    @classmethod
    async def register(cls, id: int, rating: int, balance: int, username: str, session: AsyncSession) -> None:
        if await cls.is_register(id, session):
            return
        sobj = cls(id=id, rating=rating, balance=balance, username=username)
        session.add(sobj)
        await session.commit()

    @classmethod
    async def obj(cls, id: int, session: AsyncSession):
        if not session.is_active:
            try:
                await session.begin()
            except Exception as e:
                print(e)
        _ = await session.execute(select(cls).where(cls.id == id))
        return _.scalar()
    
    @classmethod
    async def delete(cls, id: int, session: AsyncSession) -> None:
        if not session.is_active:
            try:
                await session.begin()
            except Exception as e:
                print(e)
        stmt = delete(cls).where(cls.id == id)
        await session.execute(stmt)
        await session.commit()

    @classmethod
    async def is_register(cls, id: int, session: AsyncSession) -> bool:
        if not session.is_active:
            try:
                await session.begin()
            except Exception as e:
                print(e)
        result = await session.execute(select(cls).filter_by(id=id))
        sobj = result.first()
        if sobj:
            return True
        else:
            return False
    # obj = get
    # delete
    # register
    # __contains__ = is_register
    

class Deals(SqlAlchemyBase):
    __tablename__ = "deals"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    buyer_id = Column(BigInteger, ForeignKey("users.id"))
    seller_id = Column(BigInteger, ForeignKey("sellers.id"))
    acc_id = Column(BigInteger, ForeignKey("accounts.id"), unique=True)
    date = Column(BigInteger)
    garant = Column(Boolean)
    payment_status = Column(INTEGER)
    buyer = relationship("Users", back_populates="deals")
    seller = relationship("Sellers", back_populates="deals")
    acc = relationship("Accounts", back_populates="deal")


    @classmethod
    async def register(cls, buyer_id: int, seller_id: int, acc_id: int, date: int, garant: bool, payment_status: int, session: AsyncSession) -> None:
        sobj = cls(buyer_id=buyer_id, seller_id=seller_id, acc_id=acc_id, date=date, garant=garant, payment_status=payment_status)
        session.add(sobj)
        await session.commit()

    @classmethod
    async def obj(cls, id: int, session: AsyncSession):
        if not session.is_active:
            try:
                await session.begin()
            except Exception as e:
                print(e)
        _ = await session.execute(select(cls).where(cls.id == id))
        return _.scalar()
    
    @classmethod
    async def delete(cls, id: int, session: AsyncSession) -> None:
        if not session.is_active:
            try:
                await session.begin()
            except Exception as e:
                print(e)
        stmt = delete(cls).where(cls.id == id)
        await session.execute(stmt)
        await session.commit()
        
    @classmethod
    async def get_all(cls, session: AsyncSession) -> list:
        if not session.is_active:
            try:
                await session.begin()
            except Exception as e:
                print(e)

        result = await session.execute(select(cls))
        sobjs = result.scalars().all()

        return sobjs

    @classmethod
    async def is_register(cls, id: int, session: AsyncSession) -> bool:
        if not session.is_active:
            try:
                await session.begin()
            except Exception as e:
                print(e)
        result = await session.execute(select(cls).filter_by(id=id))
        sobj = result.first()
        if sobj:
            return True
        else:
            return False
    # obj = get +
    # register +
    # __contains__ = is_register -
    # get_all +
    # delete +
    
class Accounts(SqlAlchemyBase):
    __tablename__ = "accounts"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    shop = Column(String)
    price = Column(FLOAT)
    description = Column(String)
    data = Column(String)
    view_type = Column(Boolean)
    name = Column(String)
    deal = relationship("Deals", back_populates="acc", lazy="selectin", uselist=False)


    @classmethod
    async def register(cls, shop: str, price: float, description: str, data: str, view_type: bool, name: str, session: AsyncSession) -> None:
        sobj = cls(shop=shop,price=price,description=description,data=data,view_type=view_type,name=name)
        session.add(sobj)
        await session.commit()

    @classmethod
    async def obj(cls, id: int, session: AsyncSession):
        if not session.is_active:
            try:
                await session.begin()
            except Exception as e:
                print(e)
        _ = await session.execute(select(cls).where(cls.id == id))
        return _.scalar()
    
    @classmethod
    async def delete(cls, id: int, session: AsyncSession) -> None:
        if not session.is_active:
            try:
                await session.begin()
            except Exception as e:
                print(e)
        stmt = delete(cls).where(cls.id == id)
        await session.execute(stmt)
        await session.commit()
        
    @classmethod
    async def get_all(cls, session: AsyncSession) -> list:
        if not session.is_active:
            try:
                await session.begin()
            except Exception as e:
                print(e)

        result = await session.execute(select(cls))
        sobjs = result.scalars().all()

        return sobjs
    
    @classmethod
    async def is_register(cls, id: int, session: AsyncSession) -> bool:
        if not session.is_active:
            try:
                await session.begin()
            except Exception as e:
                print(e)
        result = await session.execute(select(cls).filter_by(id=id))
        sobj = result.first()
        if sobj:
            return True
        else:
            return False
    
    # obj = get +
    # register + 
    # __contains__= is_register +
    # get_all +
    # delete +


def testing_DB():
    pass
    # seller = 
    # user = 

    # chat_1 = 
    # deal_1 = 
    # acc_1 = 

    # deal_2 =
    # acc_2 = 

    # chat_3 =
    # deal_3 =
    # acc_3 = 


if __name__ == "__main__":
    testing_DB()
from __future__ import annotations
import asyncio
from sqlalchemy import Column, BigInteger, String, INTEGER, FLOAT, ForeignKey, select, delete, Boolean, update
from models.db import SqlAlchemyBase, session_db, global_init
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship


class Chats(SqlAlchemyBase):
    __tablename__ = "chats"

    id: int = Column(BigInteger, primary_key=True)
    user_id: int = Column(BigInteger, ForeignKey("users.id"))
    seller_id: id = Column(BigInteger, ForeignKey("sellers.id"))
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
    async def obj(cls, id: int, session: AsyncSession) -> Chats:
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
        obj = cls(id=id, username=username)
        session.add(obj)
        await session.commit()

    @classmethod
    async def obj(cls, id: int, session: AsyncSession) -> Users:
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

    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
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
    async def register(cls, buyer_id: int, seller_id: int, acc_id: int, date: int, garant: bool, payment_status: int,
                       session: AsyncSession) -> None:
        sobj = cls(buyer_id=buyer_id, seller_id=seller_id, acc_id=acc_id, date=date, garant=garant,
                   payment_status=payment_status)
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

    # obj = get +
    # register +
    # __contains__ = is_register -
    # get_all +
    # delete +


class Accounts(SqlAlchemyBase):
    __tablename__ = "accounts"
    id: int = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    shop: str = Column(String)
    price: float = Column(FLOAT)
    description: str = Column(String)
    data: str = Column(String)
    view_type: bool = Column(Boolean)
    name: str = Column(String)
    deal = relationship("Deals", back_populates="acc", lazy="selectin", uselist=False)

    @classmethod
    async def register(cls, shop: str, price: float, description: str, data: str, view_type: bool, name: str,
                       session: AsyncSession) -> None:
        sobj = cls(shop=shop, price=price, description=description, data=data, view_type=view_type, name=name)
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
        objs = result.scalars().all()

        return objs

    # obj = get +
    # register +
    # __contains__= is_register +
    # get_all +
    # delete +


@session_db
async def test(session: AsyncSession):
    await Sellers.register(id=1, rating=0, balance=0, username="test", session=session)
    await Accounts.register(shop="Goggle", price=100.0, description="test description1",
                            data="test data1", view_type=True, name="youtube",
                            session=session)
    await Accounts.register(shop="Facebook", price=1200.0, description="test description2",
                            data="test data2", view_type=True, name="account",
                            session=session)
    await Accounts.register(shop="Amazon", price=1050.0, description="test description3",
                            data="test data3", view_type=True, name="AWS",
                            session=session)
    await Accounts.register(shop="Netflix", price=1020.0, description="test description4",
                            data="test data4", view_type=True, name="account",
                            session=session)
    await Accounts.register(shop="Goggle", price=10089.0, description="test description5",
                            data="test data5", view_type=True, name="AWS",
                            session=session)
    await Deals.register(buyer_id=6989531851, seller_id=1, acc_id=0, date=2345678, garant=True, payment_status=3,
                         session=session)
    await Deals.register(buyer_id=6989531851, seller_id=1, acc_id=1, date=23456780, garant=True, payment_status=2,
                         session=session)
    await Deals.register(buyer_id=6989531851, seller_id=1, acc_id=2, date=23456730, garant=False, payment_status=1,
                         session=session)
    await Deals.register(buyer_id=6989531851, seller_id=1, acc_id=3, date=234567823, garant=True, payment_status=0,
                         session=session)
    await Deals.register(buyer_id=6989531851, seller_id=1, acc_id=4, date=234567810938, garant=False, payment_status=3,
                         session=session)


if __name__ == "__main__":
    asyncio.run(test())

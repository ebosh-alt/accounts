from sqlalchemy import Column, BigInteger, String, INTEGER, FLOAT, ForeignKey, select, delete, Boolean, update
from models.db import SqlAlchemyBase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship


class Chats(SqlAlchemyBase):
    __tablename__ = "chats"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    seller_id = Column(BigInteger, ForeignKey("sellers.id"))

    user = relationship("Users", back_populates="chats")
    seller = relationship("Sellers", back_populates="chats")

    # obj = get
    # delete
    # register
    # __contains__
    

class Users(SqlAlchemyBase):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    username = Column(String)

    chats = relationship("Chats", back_populates="user", lazy="selectin")
    deals = relationship("Deals", back_populates="buyer", lazy="selectin")

    # obj = get
    # delete
    # register
    # __contains__
    # get_all

    

class Sellers(SqlAlchemyBase):
    __tablename__ = "sellers"

    id = Column(BigInteger, primary_key=True)
    rating = Column(BigInteger)
    balance = Column(BigInteger)
    username = Column(String)

    chats = relationship("Chats", back_populates="seller", lazy="selectin")
    deals = relationship("Deals", back_populates="seller", lazy="selectin")

    # obj = get
    # register
    # __contains__
    

class Deals(SqlAlchemyBase):
    __tablename__ = "deals"

    id = Column(BigInteger, primary_key=True)
    buyer_id = Column(BigInteger, ForeignKey("users.id"))
    seller_id = Column(BigInteger, ForeignKey("sellers.id"))
    acc_id = Column(BigInteger, ForeignKey("accounts.id"), unique=True)
    date = Column(BigInteger)
    garant = Column(Boolean)
    payment_status = Column(INTEGER)

    buyer = relationship("Users", back_populates="deals")
    seller = relationship("Sellers", back_populates="deals")
    acc = relationship("Accounts", back_populates="deal")

    # obj = get
    # register
    # __contains__
    # get_all
    
class Accounts(SqlAlchemyBase):
    __tablename__ = "accounts"

    id = Column(BigInteger, primary_key=True)
    shop = Column(String)
    price = Column(FLOAT)
    description = Column(String)
    data = Column(String)
    view_type = Column(Boolean)
    name = Column(String)
    
    deal = relationship("Deals", back_populates="acc", lazy="selectin", uselist=False)

    # obj = get
    # register
    # __contains__
    # get_all
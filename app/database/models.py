from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy.ext.asyncio import (AsyncAttrs, async_sessionmaker,
                                    create_async_engine)

from config import ENGINE, ECHO

engine = create_async_engine(url=ENGINE, echo=ECHO)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class User(Base):
    __tablename__ = 'users'

    tg_username: Mapped[str]
    tg_id = mapped_column(BigInteger)
    cart_relationship: Mapped['Cart'] = relationship(
        back_populates='user_relationship'
    ) #Пользователь удаляется удаляется и корзина(Корзина живет определенное количество времени?)


class Category(Base):
    __tablename__ = 'categories'
    name: Mapped[str] = mapped_column(String(80), unique=True)

    item_relationship: Mapped[list['Item']] = relationship(
        back_populates='category_relationship'
    )


class Item(Base):
    __tablename__ = 'items'
    
    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str] = mapped_column(String(200))
    photo: Mapped[str] = mapped_column(String(200))
    price: Mapped[int] = mapped_column()
    category: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    
    category_relationship: Mapped['Category'] = relationship(
        back_populates='item_relationship'
    )
    cart_relationship: Mapped[list['Cart']] = relationship(
        back_populates='item_relationship')


class Cart(Base):
    __tablename__ = 'cart'
    
    user: Mapped[int] = mapped_column(ForeignKey('users.id'))
    item: Mapped[int] = mapped_column(ForeignKey('items.id'))
    
    user_relationship: Mapped['User'] = relationship(
        back_populates='cart_relationship'
    )
    item_relationship: Mapped[list['Item']] = relationship(
        back_populates='cart_relationship'
    )


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
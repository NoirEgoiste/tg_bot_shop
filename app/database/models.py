from sqlalchemy import BigInteger, DateTime, Float, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase

class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now)
 


class Product(Base):
    __tablename__ = "Product"
    
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
    image: Mapped[str] = mapped_column(String(150))


# class User(Base):
#     __tablename__ = 'users'

#     tg_username: Mapped[str]
#     tg_id = mapped_column(BigInteger)
#     cart_relationship: Mapped['Cart'] = relationship(
#         back_populates='user_relationship'
#     )

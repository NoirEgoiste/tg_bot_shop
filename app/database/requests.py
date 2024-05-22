from sqlalchemy import select, update, delete

from app.database.models import User, Category, Item, Cart
from app.database.models import async_session


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()

async def get_users():
    async with async_session() as session:
        users = await session.scalars(select(User))
        return users


async def set_item(data):
    async with async_session() as session:
        session.add(Item(**data))
        await session.commit()


async def get_categories():
    async with async_session() as session:
        categories = await session.scalars(select(Category))
        return categories


async def get_items_by_category(category_id: int):
    async with async_session() as session:
        items = await session.scalars(
            select(Item).where(Item.category == category_id)
        )
        return items


async def get_items_by_id(item_id: int):
    async with async_session() as session:
        item = await session.scalar(
            select(Item).where(Item.id == item_id)
        )
        return item

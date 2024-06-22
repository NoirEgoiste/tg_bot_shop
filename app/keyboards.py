from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton,)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_categories, get_items_by_category

main_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Catalog", callback_data="catalog")],
    [InlineKeyboardButton(text="Cart", callback_data="my_cart"),
    InlineKeyboardButton(text="Contacts", callback_data="contacts")
     ],
])

to_main_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="My cart", callback_data="to_cart")],
    [InlineKeyboardButton(text="Main catalog", callback_data="catalog")]])


async def delete_from_cart_keyboard(order_id):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Remove from cart",
                                      callback_data=f"delete_{order_id}"))
    return keyboard.adjust(2).as_markup()


async def cart_keyboard(order_id):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Checkout",
                                      callback_data=f"order_{order_id}"))
    keyboard.add(InlineKeyboardButton(text="Back", callback_data="catalog"))
    return keyboard.adjust(2).as_markup()


async def categories_keyboard():
    all_categories = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(
            text=category.name,
            callback_data=f"category_{category.id}"))
    keyboard.add(InlineKeyboardButton(text="To main",
                                      callback_data="to_main"))
    return keyboard.adjust(2).as_markup()


async def items_keyboard(category_id: int):
    items = await get_items_by_category(category_id)
    keyboard = InlineKeyboardBuilder()
    for item in items:
        print(item.name, item.id)
        keyboard.add(InlineKeyboardButton(text=item.name,
                                          callback_data=f"item_{item.id}"))

    return keyboard.adjust(2).as_markup()

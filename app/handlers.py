from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

import app.keyboards as keyboards
from app.database.requests import get_items_by_id, set_user, set_cart, \
    get_cart, delete_cart

router = Router()

@router.message(CommandStart())
@router.callback_query(F.data == "to_main")
async def cmd_start(message: Message | CallbackQuery):
    if isinstance(message, Message):
        await set_user(message.from_user.id)
        await message.answer("Welcome to internet shop!",
                         reply_markup=keyboards.main_keyboard)
    else:
        await message.answer("Back to main menu")
        await message.message.answer("Welcome to internet shop!",
                                        reply_markup=keyboards.to_main_keyboard)

@router.callback_query(F.data == "catalog")
async def catalog(callback: CallbackQuery):
    await callback.message.edit_text("Choose, category",
                                     reply_markup=await keyboards.categories_keyboard())


@router.callback_query(F.data.startswith("category_"))
async def category(callback: CallbackQuery):
    category_id = int(callback.data.split("_")[1])
    await callback.message.edit_text("Choose a product",
                                  reply_markup=await keyboards.items_keyboard(category_id))


@router.callback_query(F.data.startswith("item_"))
async def item(callback: CallbackQuery):
    item = await get_items_by_id(int(callback.data.split("_")[1]))
    await callback.message.answer_photo(photo=item.photo, caption=f"Product Name: {item.name}\n\n"
                                          f"Description: {item.description}\n"
                                          f"Cost: ${item.price}",
                                        reply_markup=await keyboards.cart_keyboard(item.id))


@router.callback_query(F.data.startswith("cart"))
async def cart(callback: CallbackQuery):
    order_id = await set_cart(callback.from_user.id,int(callback.data.split("_")[1]))
    await callback.message.answer("Product added to cart",
                                  reply_markup=await keyboards.cart_keyboard(order_id))


@router.callback_query(F.data == "my_cart")
async def my_cart(callback: CallbackQuery):
    items = await get_cart(callback.from_user.id)
    for item in items:
        await get_items_by_id(item.id)
        await (callback.message.
               answer_photo(photo=item.photo,
                            caption=f"Product Name: {item.name}\n\n"
                                    f"Description: {item.description}\n"
                                    f"Cost: ${item.price}",
                            reply_markup=await keyboards.delete_from_cart_keyboard(item.id)))


@router.callback_query(F.data.startwith("delete_"))
async def delete_from_cart(callback: CallbackQuery):
    await delete_cart(callback.from_user.id, int(callback.data.split("_")[1]))
    await callback.message.answer("Item removed")
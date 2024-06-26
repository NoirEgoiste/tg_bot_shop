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
    print(message.from_user.id, message.from_user.username)
    if isinstance(message, Message):
        await set_user(
            message.from_user.id, message.from_user.username
        )
        await message.answer(
            "Welcome to internet shop!",
            reply_markup=keyboards.main_keyboard
        )
    else:
        await message.answer("Back to main menu")
        await message.message.answer(
            "Welcome to internet shop!",
            reply_markup=keyboards.to_main_keyboard
        )


@router.callback_query(F.data == "catalog")
async def catalog(callback: CallbackQuery):
    await callback.message.edit_text(
        "Choose, category",
        reply_markup=await keyboards.categories_keyboard()
    )


@router.callback_query(F.data.startswith("category_"))
async def category(callback: CallbackQuery):
    category_id = int(callback.data.split("_")[1])
    await callback.message.edit_text(
        "Choose a product",
        reply_markup=await keyboards.items_keyboard(category_id))


@router.callback_query(F.data.startswith("item_"))
async def item(callback: CallbackQuery):
    item_id = await get_items_by_id(int(callback.data.split("_")[1]))
    await callback.message.answer_photo(
        photo=item_id.photo,
        caption=f"Product Name: {item_id.name}\n\n"
                f"Description: {item_id.description}\n"
                f"Cost: ${item_id.price}",
        reply_markup=await keyboards.cart_keyboard(item_id.id))


@router.callback_query(F.data.startswith("order_"))
async def cart(callback: CallbackQuery):
    order_id = await set_cart(
        callback.from_user.id,
        callback.data.split("_")[1])

    await callback.answer(
        "Added to cart",
        reply_markup=await keyboards.cart_keyboard(order_id))


@router.callback_query(F.data == "my_cart")
async def my_cart(callback: CallbackQuery):
    user_cart = await get_cart(callback.from_user.id)
    if not user_cart:
        await callback.message.answer("Your cart is empty")

    for c_item in user_cart:
        items = await get_items_by_id(c_item.item)
        await (
            callback.message.answer_photo(
                photo=items.photo,
                caption=f"Product Name: {items.name}\n\n"
                        f"Description: {items.description}\n"
                        f"Cost: ${items.price}",
                reply_markup=await keyboards.
                delete_from_cart_keyboard(items.id)
            )
        )


@router.callback_query(F.data.startwith("delete_"))
async def delete_from_cart(callback: CallbackQuery):
    await delete_cart(callback.from_user.id,
                      callback.data.split("_")[1])
    await callback.message.delete()
    await callback.message.answer("Item removed")

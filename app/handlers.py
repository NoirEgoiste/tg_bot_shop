from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

import app.keyboards as keyboards
from app.database.requests import get_items_by_id, set_user

router = Router()

@router.message(CommandStart())
@router.callback_query(F.data == "to_main")
async def cmd_start(message: Message | CallbackQuery):
    if isinstance(message, Message):
        await set_user(message.from_user.id)
        await message.answer("Welcome to internet shop!",
                         reply_markup=keyboards.main_keyboard)
    else:
        await message.message.edit_text("Welcome to internet shop!",
                                        reply_markup=keyboards.main_keyboard)

@router.callback_query(F.data == "catalog")
async def catalog(callback: CallbackQuery):
    await callback.message.edit_text("Choose, category",
                         reply_markup=await keyboards.categories())


@router.callback_query(F.data.startswith("category_"))
async def category(callback: CallbackQuery):
    category_id = int(callback.data.split("_")[1])
    await callback.message.edit_text("Choose a product",
                                  reply_markup=await keyboards.items(category_id))


@router.callback_query(F.data.startswith("item_"))
async def item(callback: CallbackQuery):
    item = await get_items_by_id(int(callback.data.split("_")[1]))
    await callback.message.edit_text(text=f"{item.name}\n\n"
                                          f"{item.description}\n\n "
                                          f"Cost: ${item.price}",
                                  reply_markup=keyboards.to_main_keyboard)

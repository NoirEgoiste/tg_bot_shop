from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import CommandStart, Command, or_f
from aiogram.types import Message, CallbackQuery

from app.filters.chat_type_filter import ChatTypeFilter
from app.keyboards.reply_keyboards import start_kb, del_kb, start_kb2, start_kb3, start_kb4


user = Router()
user.message.filter(ChatTypeFilter([ChatType.PRIVATE]))


@user.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(text="Привет я виртуальный помощник!", reply_markup=start_kb4)


@user.message(or_f(Command("menu"), F.text.lower() == "меню"))
async def main_menu(message: Message):
    await message.answer(text="Вот меню:", reply_markup=del_kb)


@user.message(or_f(Command("about"), F.text.lower() == "о магазине"))
async def about(message: Message):
    await message.answer(text="О нас:")


@user.message(or_f(Command("payment"), F.text.lower() == "оплата"))
async def payment(message: Message):
    await message.answer(text="Оплата:")


@user.message(or_f(Command("shipment"), F.text.lower() == "доставка"))
async def shipment(message: Message):
    await message.answer(text="Доставка:")

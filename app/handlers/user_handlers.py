from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import Command, or_f
from aiogram.types import Message, CallbackQuery

from app.filters.chat_type_filter import ChatTypeFilter

user = Router()
user.message.filter(ChatTypeFilter([ChatType.PRIVATE]))


@user.message(or_f(Command("menu"), F.text.lower() == "меню"))
async def main_menu(message: Message):
    await message.answer(text="Hello")


@user.message(or_f(Command("about"), F.text.lower() == "о нас"))
async def about(message: Message):
    await message.answer(text="About")


@user.message(or_f(Command("payment"), F.text.lower() == "оплата"))
async def payment(message: Message):
    await message.answer(text="Payment")


@user.message(or_f(Command("shipment"), F.text.lower() == "доставка"))
async def shipment(message: Message):
    await message.answer(text="Magic filter")

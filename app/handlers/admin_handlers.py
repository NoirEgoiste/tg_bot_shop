from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command, Filter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.filters.chat_type_filter import ChatTypeFilter, IsAdmin
from app.keyboards.keyboards_creater import get_keyboard

admin = Router()
admin.message.filter(ChatTypeFilter(ChatType.PRIVATE), IsAdmin())
admin_btns = ["Добавить товар", "Изменить товар", "Удалить товар", "Посмотреть товар",]

ADMIN_KB = get_keyboard(
    *admin_btns,
    placeholder="Выбирите действие",
    sizes=(2, 1, 1)
)

@admin.message(Command("admin"))
async def add_product(message: Message):
    await message.answer("Выберите действие", reply_markup=await ADMIN_KB)


@admin.message(F.text == "Изменить товар")
async def change_product(message: Message):
    await message.answer("ОК, вот список товаров")


@admin.message(F.text == "Удалить товар")
async def delete_product(message: Message):
    await message.answer("Выберите товар(ы) для удаления")


@admin.message(F.text == "Посмотреть товар")
async def starring_at_product(message: Message):
    await message.answer("ОК, вот список товаров")


@admin.message(F.text == "Добавить товар")
async def change_product(message: Message):
    await message.answer("Введите название товара", reply_markup=ReplyKeyboardRemove())


@admin.message(Command("отмена"))
@admin.message(F.text.casefold() == "отмена")
async def cancel_handler(message: Message) -> None:
    await message.answer("Действие отмены", reply_markup=ADMIN_KB)


@admin.message(Command("назад"))
@admin.message(F.text.casefold() == "назад")
async def cancel_handler(message: Message) -> None:
    await message.answer("Вы вернулись к прошлому шагу")


@admin.message(F.text)
async def add_name(message: Message):
    pass

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command, Filter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import app.keyboards as keyboards
from app.database.requests import get_users, set_item

admin = Router()


class NewsLetter(StatesGroup):
    message = State()
    # confirm = State()


class AddItem(StatesGroup):
    name = State()
    description = State()
    category = State()
    photo = State()
    price = State()


class AdminProtect(Filter):
    async def __call__(self, message: Message):
        return message.from_user.id in [239721784] # Tg admin id's

@admin.message(AdminProtect(), Command("admin"))
async def admin_panel(message: Message):
    await message.answer(f"Commands: \n"
                         f"/newsletter\n"
                         f"/add_item\n")


@admin.message(AdminProtect(), Command("newsletter"))
async def newsletter(message: Message, state: FSMContext):
    await state.set_state(NewsLetter.message)
    await message.answer("Send a message, for all users")


@admin.message(AdminProtect(), NewsLetter.message)
async def newsletter_message(message: Message, state: FSMContext):
    await message.answer("Please wait... Mailing in progress")
    for user in await get_users():
        try:
            await message.send_copy(chat_id=user.tg_id)
        except:
            pass
    await message.answer("Mailing Ended")
    await state.clear()


@admin.message(AdminProtect(), Command("add_item"))
async def add_item(message: Message, state: FSMContext):
    await state.set_state(AddItem.name)
    await message.answer("Enter Item name")


@admin.message(AdminProtect(), AddItem.name)
async def add_item_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddItem.description)
    await message.answer("Enter Item description")


@admin.message(AdminProtect(), AddItem.description)
async def add_item_category(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(AddItem.category)
    await message.answer("Select or Add Item category",
                         reply_markup=await keyboards.categories())


@admin.callback_query(AdminProtect(), AddItem.category)
async def add_item_category(callback: CallbackQuery, state: FSMContext):
    await state.update_data(category=callback.data.split("_")[1])
    await state.set_state(AddItem.photo)
    await callback.message.answer("Enter Item photo")


@admin.message(AdminProtect(), AddItem.photo, F.photo)
async def add_item_photo(message: Message, state: FSMContext):
    await state.update_data(name=message.photo[-1].file_id)
    await state.set_state(AddItem.price)
    await message.answer("Enter Item price")



@admin.message(AdminProtect(), AddItem.price)
async def add_item_price(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await set_item(await state.get_data())
    await message.answer("Item successfully added")
    await state.clear()

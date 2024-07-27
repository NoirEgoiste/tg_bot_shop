from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, \
    KeyboardButton
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.engine import session_maker
from app.database.models import Product
from app.filters.chat_type_filter import ChatTypeFilter, IsAdmin
from app.keyboards.keyboards_creater import get_keyboard
from app.middlewares.db import DataBaseSession

admin = Router()
admin.message.filter(ChatTypeFilter(ChatType.PRIVATE), IsAdmin())
admin.message.middleware(DataBaseSession(session_pool=session_maker))

admin_btns = ["Добавить товар", "Изменить товар", "Удалить товар",
              "Посмотреть товар", ]

# ADMIN_KB = get_keyboard(
#     admin_btns,
#     placeholder="Выбирите действие",
#     sizes=(2, 2)
# )


ADMIN_KB = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Добавить товар"),
         KeyboardButton(text="Изменить товар")],
        [KeyboardButton(text="Удалить товар"),
         KeyboardButton(text="Посмотреть товар")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие")

BACK_KB = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="назад"),
         KeyboardButton(text="отмена")],
    ],
    resize_keyboard=True
)


class AddProduct(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()

    texts = {
        'AddProduct:name': 'Введите название заново:',
        'AddProduct:description': 'Введите описание заново:',
        'AddProduct:price': 'Введите стоимость заново:',
        'AddProduct:image': 'Этот стейт последний, поэтому...',
    }


@admin.message(Command("admin"))
async def add_product(message: Message):
    await message.answer("Выберите действие", reply_markup=ADMIN_KB)


@admin.message(F.text == "Изменить товар")
async def change_product(message: Message, state: FSMContext):
    await message.answer("ОК, вот список товаров")


@admin.message(F.text == "Удалить товар")
async def delete_product(message: Message, state: FSMContext):
    await message.answer("Выберите товар(ы) для удаления")


@admin.message(F.text == "Посмотреть товар")
async def starring_at_product(message: Message, state: FSMContext):
    await message.answer("ОК, вот список товаров")


@admin.message(StateFilter(None), F.text == "Добавить товар")
async def change_product(message: Message, state: FSMContext):
    await message.answer("Введите название товара",
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddProduct.name)


@admin.message(StateFilter("*"), Command("отмена"))
@admin.message(StateFilter("*"), F.text.casefold() == "отмена")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("Действия отменены", reply_markup=ADMIN_KB)


@admin.message(StateFilter('*'), Command("назад"))
@admin.message(StateFilter('*'), F.text.casefold() == "назад")
async def back_step_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state == AddProduct.name:
        await message.answer(
            'Предыдущего шага нет, '
            'или введите название товара или напишите "отмена"')
        return

    previous = None
    for step in AddProduct.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(
                f"Ок, вы вернулись к прошлому шагу "
                f"\n {AddProduct.texts[previous.state]}")
            return
        previous = step


# TODO Добавить обработку ошибок.
@admin.message(AddProduct.name, F.text)
async def add_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите описание товара", reply_markup=BACK_KB)
    await state.set_state(AddProduct.description)


@admin.message(AddProduct.description, F.text)
async def add_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Введите стоимость товара", reply_markup=BACK_KB)
    await state.set_state(AddProduct.price)


@admin.message(AddProduct.price, F.text)
async def add_price(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer("Загрузите изображение товара", reply_markup=BACK_KB)
    await state.set_state(AddProduct.image)


@admin.message(AddProduct.image, F.photo)
async def add_image(
        message: Message,
        state: FSMContext,
        session: AsyncSession
):
    await state.update_data(image=message.photo[-1].file_id)
    data = await state.get_data()
    session.add(Product(**data))
    await session.commit()
    await message.answer(
        "Нажмите продолжить если введенная информация верна",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="назад"),
                 KeyboardButton(text="отмена")],
                [KeyboardButton(text="продолжить")],
            ],
            resize_keyboard=True
)
    )
    await message.answer("Товар добавлен", reply_markup=ADMIN_KB)
    await state.clear()

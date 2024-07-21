from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardRemove, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from app.keyboards.keyboards_creater import get_keyboard

start_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Меню"),
     KeyboardButton(text="О магазине"), ],
    [KeyboardButton(text="Доставка"),
     KeyboardButton(text="Оплата"), ]
],
    resize_keyboard=True,
    input_field_placeholder="Выберите вариант",
)

del_kb = ReplyKeyboardRemove()

start_kb2 = ReplyKeyboardBuilder()
start_kb2.add(
    KeyboardButton(text="Меню"),
    KeyboardButton(text="О магазине"),
    KeyboardButton(text="Доставка"),
    KeyboardButton(text="Оплата"),
)
start_kb2.adjust(2, 2)

start_kb3 = ReplyKeyboardBuilder()
start_kb3.attach(start_kb2)
start_kb3.row(KeyboardButton(text="Hello"))

start_kb4 = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Создать опрос",
                    request_poll=KeyboardButtonPollType())],
    [KeyboardButton(text="☎️ Отправить номер телефона", request_contact=True),
     KeyboardButton(text="🗺️ Отправить местоположение",
                    request_location=True), ]
], resize_keyboard=True, )

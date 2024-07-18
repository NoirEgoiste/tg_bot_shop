from string import punctuation

from aiogram import Router
from aiogram.enums import ChatType
from aiogram.types import Message

from app.filters.chat_type_filter import ChatTypeFilter

group = Router()
group.message.filter(ChatTypeFilter([ChatType.GROUP]))

restricted_words = {"кабан", "цирк", "выхухоль"}


def clean_text(text: str):
    return text.translate(str.maketrans("", "", punctuation))


@group.message()
async def cleaner(message: Message):
    if restricted_words.intersection(clean_text(message.text.lower()).split()):
        await message.answer(f"{message.from_user.username}, "
                             f"соблюдайте правила в чате!")
        await message.delete()

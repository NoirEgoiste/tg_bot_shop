from string import punctuation

from aiogram import F, Router
from aiogram.filters import CommandStart, Command, or_f
from aiogram.types import Message

group = Router()

restricted_words = {"кабан", "цирк", "выхухоль"}


def clean_text(text: str):
    return text.translate(str.maketrans("", "", punctuation))


@group.message()
async def cleaner(message: Message):
    if restricted_words.intersection(clean_text(message.text.lower()).split()):
        await message.answer(f"{message.from_user.username}, "
                             f"соблюдайте правила в чате!")
        await message.delete()

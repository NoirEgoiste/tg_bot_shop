from string import punctuation

from aiogram import Bot, Router, F
from aiogram.enums import ChatType
from aiogram.types import Message
from aiogram.filters import Command

from app.filters.chat_type_filter import ChatTypeFilter

group = Router()
group.message.filter(ChatTypeFilter([ChatType.GROUP, ChatType.SUPERGROUP]))

restricted_words = {"кабан", "цирк", "выхухоль"}


@group.message(Command("admin"))    
async def get_admins(message: Message, bot: Bot):
    chat_id = message.chat.id
    admins_list = await bot.get_chat_administrators(chat_id)
    admins_list = [
        member.user.id
        for member in admins_list
        if member.status == "creator" or member.status == "administarator" and member.is_bot == False
    ]
    bot.my_admins_list = admins_list
    if message.from_user.id in admins_list:
        await message.delete()


def clean_text(text: str):
    return text.translate(str.maketrans("", "", punctuation))


@group.message()
async def cleaner(message: Message):
    if restricted_words.intersection(clean_text(message.text.lower()).split()):
        await message.answer(f"{message.from_user.username}, "
                             f"соблюдайте правила в чате!")
        await message.delete()

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def get_keyboard(
    btns: list[str],
    placeholder: str = None,
    request_contact: int = None,
    request_location: int = None,
    sizes: tuple[int] = (2, ),
):
    """
    Creates reply keyboard 
    
    Exaple
    get_keyboard(
        "Menu",
        "About",
        "Payment",
        placeholder="Add your place holder",
        request_contact=4
        request_location=5
        sizes=(2, 1, 2)
        
    )
    

    Args:
        placeholder (str, optional): add your placeholder to input. Defaults to None.
        request_contact (int, optional): Index of button position Defaults to None.
        request_location (int, optional): Index of button position. Defaults to None.
        sizes (tuple[int], optional): Size for buttons placement. Defaults to (2,).
    """
    keyboard = ReplyKeyboardBuilder()
    
    for index, text in enumerate(btns, start=0):
    
        if request_contact and request_contact == index:
            keyboard.add(KeyboardButton(text=text, request_contact=True))
        elif request_location and request_location == index:
            keyboard.add(KeyboardButton(text=text, request_location=True))
        else:
            keyboard.add(KeyboardButton(text=text))
    
    return keyboard
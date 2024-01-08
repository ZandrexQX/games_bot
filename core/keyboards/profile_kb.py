from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_profile_kb():
    kb_builder = ReplyKeyboardBuilder()

    kb_builder.button(text='Профиль')
    return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True,
                         input_field_placeholder='Ваш профиль')

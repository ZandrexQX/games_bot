from aiogram.utils.keyboard import InlineKeyboardBuilder
import os, datetime
from Aiogram.games_bot.core.utils.dbconnect import Database

def place_kb():
    db = Database(os.getenv('DATABASE'))
    places = db.db_select_all('place')
    kb = InlineKeyboardBuilder()

    for place in places:
        kb.button(text=f'{place[1]}', callback_data=f'{place[0]}')
    kb.adjust(1)
    return kb.as_markup()

def date_kb():
    kb = InlineKeyboardBuilder()
    current_date = datetime.date.today()
    for i in range(7):
        current_date += datetime.timedelta(days=1)
        kb.button(text=f'{current_date.strftime("%d.%m")}', callback_data=f"{current_date.strftime('%d.%m.%y')}")
    kb.adjust(1)
    return kb.as_markup()

def time_kb():
    kb = InlineKeyboardBuilder()
    for i in range(9, 22, 3):
        kb.button(text=f"{i}:00", callback_data=f"time_{i}:00")
    kb.adjust(1)
    return kb.as_markup()
from Aiogram.games_bot.core.keyboards.profile_kb import get_profile_kb
from aiogram import Bot
from aiogram.types import Message
from games_bot.core.utils.dbconnect import Database
import os


async def view_profile(message: Message, bot: Bot):
    db = Database(os.getenv('DATABASE'))
    games = db.db_select_column('games', 'status', 0)
    if (games):
        await bot.send_message(message.from_user.id, f'<b>Актуальные игры:</b>')
        for game in games:
            await bot.send_message(message.from_user.id, f'Игра состоится: {game[2]} в {game[3]}\n'
                                                         f'Минимальное число участников: {game[4]}\n'
                                                         f'Максимальное число участников: {game[5]}\n'
                                                         f'Стоимость игры: {game[6]}')
    else:
        await bot.send_message(message.from_user.id, f'Игр нет')
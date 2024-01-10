import json
from Aiogram.games_bot.core.keyboards.register_kb import get_reg_kb
from Aiogram.games_bot.core.keyboards.profile_kb import get_profile_kb, add_sub, del_sub
from aiogram import Bot
from aiogram.types import Message
from games_bot.core.utils.dbconnect import Database
import os


async def get_start(message: Message, bot: Bot):
    db = Database(os.getenv('DATABASE'))
    users = db.select_user_id(message.from_user.id)
    if (users):
        await bot.send_message(message.from_user.id, f'<b>Привет {users[1]}.</b> 😎\n\n'
                                                     f'Ваш телефон: {users[2]}\n'
                                                     f'Ваш баланс: {users[4]}', reply_markup=get_profile_kb())
        if int(users[5]) == 0:
            await bot.send_message(message.from_user.id, f"Вы не подписаны на рассылку", reply_markup=add_sub(users[3]))
        else:
            await bot.send_message(message.from_user.id, f"Вы подписаны на рассылку", reply_markup=del_sub(users[3]))
    else:
        await bot.send_message(message.from_user.id, f'<b>Приветствуем {message.from_user.first_name}. Зарегистрируйся ниже.</b> 😎', reply_markup=get_reg_kb())

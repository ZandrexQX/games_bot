from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from Aiogram.games_bot.core.state.register import RegisterState
import re
import os
from Aiogram.games_bot.core.utils.dbconnect import Database


async def start_register(message: Message, state: FSMContext, bot: Bot):
    db = Database(os.getenv('DATABASE'))
    users = db.select_user_id(message.from_user.id)
    if users:
        await bot.send_message(message.from_user.id, f'{users[1]} уже зарегистрирован')
    else:
        await bot.send_message(message.from_user.id, f'Как к вам обращаться? 🖊')
        await state.set_state(RegisterState.regName)


async def reg_name(message: Message, state: FSMContext, bot: Bot):
    await bot.send_message(message.from_user.id, f'Приятно познакомиться {message.text}\n'
                                                 f'Теперь введите номер телефона - 🖊')

    await state.update_data(regname=message.text)
    await state.set_state(RegisterState.regPhone)


async def reg_phone(message: Message, state: FSMContext, bot: Bot):
    if re.findall('^\+?[7][-\(]?\d{3}\)?-?\d{3}-?\d{2}-?\d{2}$', message.text):
        await state.update_data(regphone=message.text)
        reg_data = await state.get_data()
        name = reg_data.get('regname')
        phone = reg_data.get('regphone')
        msg = f'Приятно познакомиться {name}\n Телефон - {phone}'
        await bot.send_message(message.from_user.id, msg)
        db = Database(os.getenv('DATABASE'))
        db.add_user(name, phone, message.from_user.id)
        await state.clear()
    else:
        await bot.send_message(message.from_user.id, f'Номер указан неверно')

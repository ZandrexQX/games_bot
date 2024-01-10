from aiogram import Bot, Dispatcher, F
import asyncio
from dotenv import load_dotenv
import os
from aiogram.filters import Command

from core.utils.commands import set_commands
from core.handlers.basic import get_start
from core.handlers.profile import view_profile, view_game, view_game_date, add_match_player, del_match_player, edit_subscription
from core.handlers.register import start_register, reg_name, reg_phone
from core.state.register import RegisterState
from core.state.statecreate import CreateState
from core.filters.isadmin import IsAdmin
from core.admin.create import create_game, select_place, select_date, select_time, select_minplayer, select_maxplayer, select_price
from core.handlers.pay import view_balance, add_balance, pay_pre_checkout_query, successful_payment
from core.admin.user_game import view_user_game, pay_game

import logging

logging.basicConfig(level=logging.WARNING, filename='bot_log.log',
                    format="[%(asctime)s] - [%(levelname)s] - "
                               "%(funcName)s:%(lineno)d - %(message)s",
                    datefmt='%d-%m-%y %H:%M:%S')
load_dotenv()

token = os.getenv('BOT_TOKEN')
admin_id = os.getenv('ID_ADMIN')

bot = Bot(token=token, parse_mode='HTML')
dp = Dispatcher()

async def start_bot(bot: Bot):
    await bot.send_message(admin_id, text='Bot started')

dp.startup.register(start_bot)
dp.message.register(get_start, Command(commands='start'))

# Регистрируем хендлеры
dp.message.register(start_register, F.text == 'Зарегистрироваться')
dp.message.register(reg_name, RegisterState.regName)
dp.message.register(reg_phone, RegisterState.regPhone)
# Регистрируем хендлеры для админов
dp.message.register(create_game, Command(commands='create'), IsAdmin())
dp.callback_query.register(select_place, CreateState.place)
dp.callback_query.register(select_date, CreateState.date)
dp.callback_query.register(select_time, CreateState.time)
dp.message.register(select_minplayer, CreateState.minplayer)
dp.message.register(select_maxplayer, CreateState.maxplayer)
dp.message.register(select_price, CreateState.price)
# Регистрируем хендлеры профиля
dp.message.register(view_game, F.text == 'Актуальные игры')
dp.callback_query.register(view_game_date, F.data.startswith('view_date_'))
dp.callback_query.register(add_match_player, F.data.startswith('add_match'))
dp.callback_query.register(del_match_player, F.data.startswith('del_match'))
# Balance
dp.message.register(view_balance, F.text == 'Баланс')
dp.callback_query.register(add_balance, F.data.startswith('add_balance'))
dp.pre_checkout_query.register(pay_pre_checkout_query)
dp.message.register(successful_payment, F.successful_payment)
# Games
dp.message.register(view_user_game, F.text == 'Мои игры')
dp.callback_query.register(pay_game, F.data.startswith('pay_game'))
# Subscription
dp.callback_query.register(edit_subscription, F.data.startswith('edit_sub'))

async def start():
    await set_commands(bot=bot)
    try:
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(start())
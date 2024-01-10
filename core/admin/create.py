from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from Aiogram.games_bot.core.state.statecreate import CreateState
from Aiogram.games_bot.core.keyboards.create_kb import place_kb, date_kb, time_kb
from Aiogram.games_bot.core.utils.dbconnect import Database
import os

async def create_game(message: Message, state: FSMContext, bot: Bot):
    await bot.send_message(message.from_user.id, f'Выберите площадку', reply_markup=place_kb())
    await state.set_state(CreateState.place)

async def select_place(call: CallbackQuery, state: FSMContext):
    await call.message.answer(f'Место игры выбрано!\n'
                              f'Дальше выберите дату', reply_markup=date_kb())
    await state.update_data(place=call.data)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer()
    await state.set_state(CreateState.date)

async def select_date(call: CallbackQuery, state: FSMContext):
    await call.message.answer(f'Дата выбрана!\n'
                              f'Дальше выберите время', reply_markup=time_kb())
    await state.update_data(date=call.data)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer()
    await state.set_state(CreateState.time)

async def select_time(call: CallbackQuery, state: FSMContext):
    await call.message.answer(f'Время выбрано!\n'
                              f'Укажите минимальное количество игроков (от 4 до 16)')
    await state.update_data(time=call.data)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer()
    await state.set_state(CreateState.minplayer)

async def select_minplayer(message: Message, state: FSMContext, bot: Bot):
    if message.text.isdigit() and 4 <= int(message.text) <= 16:
        await bot.send_message(message.from_user.id, f"Теперь укажите максимальное число игроков (до 16)")
        await state.update_data(minplayer=message.text)
        await state.set_state(CreateState.maxplayer)
    else:
        await bot.send_message(message.from_user.id, f"Я жду цифру от 4 до 16, а не {message.text}")

async def select_maxplayer(message: Message, state: FSMContext, bot: Bot):
    minplayer = await state.get_data()
    a = int(minplayer['minplayer'])
    if message.text.isdigit() and a <= int(message.text) <= 16:
        await bot.send_message(message.from_user.id, f"Теперь укажите стоимость игры")
        await state.update_data(maxplayer=message.text)
        await state.set_state(CreateState.price)
    else:
        await bot.send_message(message.from_user.id, f"Я жду цифру от {a} до 16, а не {message.text}")

async def select_price(message: Message, state: FSMContext, bot: Bot):
    if message.text.isdigit():
        await bot.send_message(message.from_user.id, f'Отлично, я записал игру')
        await state.update_data(price=message.text)
        create_data = await state.get_data()
        create_time = create_data.get('time').split('_')[1]
        db = Database(os.getenv('DATABASE'))
        db.add_game(create_data['place'], create_data['date'], create_time, create_data['minplayer'],
                    create_data['maxplayer'], create_data['price'])
        users = db.db_select_column('users', 'subscription', 1)
        for user in users:
            await bot.send_message(user[3], f"Добавлена новая игра\n"
                                            f"Дата: {create_data['date']}\n"
                                            f"Время: {create_time}\n"
                                            f"Цена: {create_data['price']}")
        await state.clear()
    else:
        await bot.send_message(message.from_user.id, f"Я жду число, а не {message.text}")
from Aiogram.games_bot.core.keyboards.profile_kb import get_profile_kb
from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from games_bot.core.utils.dbconnect import Database
from Aiogram.games_bot.core.keyboards.profile_kb import get_date_kb, add_match, del_match, add_sub, del_sub
from Aiogram.games_bot.core.utils.function import list_gamer
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

async def view_game(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, f"Выберите дату игры", reply_markup=get_date_kb())

async def view_game_date(call: CallbackQuery):
    await call.answer()
    date = call.data.split("_")[-1]
    db = Database(os.getenv('DATABASE'))
    games = db.select_games('0', date)
    if games:
        await call.message.answer('Актуальные игры:')
        for game in games:
            players = db.select_player(game[0])
            gamers = list_gamer(players)
            msg = f"Игра состоится: {game[9]} (Адрес: {game[10]})\n\n" \
                  f"{game[2]} в {game[3]}\n\n" \
                  f"Количество участников: от {game[4]} до {game[5]}\n\n" \
                  f"Стоимость игры: {game[6]}\n\n" \
                  f"{gamers}"
            if not(db.check_user(game[0], call.from_user.id)):
                await call.message.answer(msg, reply_markup=add_match(game[0], call.from_user.id))
            else:
                await call.message.answer(msg, reply_markup=del_match(game[0], call.from_user.id))
    else:
        await call.message.answer(f"В выбранную дату игр не планируется")


async def add_match_player(call: CallbackQuery):
    db = Database(os.getenv('DATABASE'))
    game = db.select_game(0, call.data.split('_')[-2])
    pattern = (game[0], call.from_user.id)
    if not db.check_user(*pattern):
        db.add_user_match(*pattern)
    players = db.select_player(game[0])
    gamers = list_gamer(players)
    msg = f"Игра состоится: {game[9]} (Адрес: {game[10]})\n\n" \
          f"{game[2]} в {game[3]}\n\n" \
          f"Количество участников: от {game[4]} до {game[5]}\n\n" \
          f"Стоимость игры: {game[6]}\n\n" \
          f"{gamers}"
    await call.message.edit_text(msg, reply_markup=del_match(*pattern))

async def del_match_player(call: CallbackQuery):
    db = Database(os.getenv('DATABASE'))
    game = db.select_game(0, call.data.split('_')[-2])
    pattern = (game[0], call.from_user.id)
    if db.check_user(*pattern):
        db.del_user_match(*pattern)
    players = db.select_player(game[0])
    gamers = list_gamer(players)
    msg = f"Игра состоится: {game[9]} (Адрес: {game[10]})\n\n" \
          f"{game[2]} в {game[3]}\n\n" \
          f"Количество участников: от {game[4]} до {game[5]}\n\n" \
          f"Стоимость игры: {game[6]}\n\n" \
          f"{gamers}"
    await call.message.edit_text(msg, reply_markup=add_match(*pattern))

async def edit_subscription(call: CallbackQuery):
    db = Database(os.getenv('DATABASE'))
    user = db.select_user_id(call.from_user.id) # тут по другому
    if int(user[5]) == 0:
        db.subscr_edit(user[3], 1)
        await call.message.edit_text(f"Вы подписаны на рассылку", reply_markup=del_sub(user[3]))
    else:
        db.subscr_edit(user[3], 0)
        await call.message.edit_text(f"Вы не подписаны на рассылку", reply_markup=add_sub(user[3]))
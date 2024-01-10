from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from games_bot.core.utils.dbconnect import Database
from Aiogram.games_bot.core.keyboards.profile_kb import get_date_kb, add_match, del_match, del_buy_match
from Aiogram.games_bot.core.utils.function import list_gamer
import os

async def view_user_game(message: Message, bot: Bot):
    db = Database(os.getenv('DATABASE'))
    games = db.user_game('0', message.from_user.id)

    if games:
        await bot.send_message(message.from_user.id, f"Вы записаны на следующие игры:")
        for game in games:
            players = db.select_player(game[0])
            gamers = list_gamer(players)
            msg = f"Игра состоится: {game[9]}  по адресу: {game[10]})\n\n" \
                  f"{game[4]} в {game[5]}\n\n" \
                  f"Стоимость игры: {game[6]}\n\n" \
                  f"🌟 Игроки: 🌟\n"\
                  f"{gamers}"
            check_pay = db.select_pay(game[0], message.from_user.id)
            if check_pay:
                await bot.send_message(message.from_user.id, msg, reply_markup=del_match(game[0], message.from_user.id))
            else:
                await bot.send_message(message.from_user.id, msg, reply_markup=del_buy_match(game[0], message.from_user.id))
    else:
        await bot.send_message(message.from_user.id, f"Вы не записаны")

async def pay_game(call: CallbackQuery):
    await call.answer()
    game_id = call.data.split("_")[-2]
    user_id = call.data.split("_")[-1]
    db = Database(os.getenv('DATABASE'))
    game = db.select_game(0, game_id)
    user = db.select_user_id(user_id)
    if int(user[4]) >= int(game[6]):
        balance_edit = int(user[4]) - int(game[6])
        db.balance_user_edit(user_id, balance_edit)
        db.balance_system(f"- {int(game[6])}", user_id)
        db.buy_game(game_id, user_id, game[6])
        await call.message.answer(f" Вы успешно оплатили. Ваш баланс: {balance_edit}")
        await call.message.edit_reply_markup(reply_markup=None)
    else:
        await call.message.answer(f"Ваш баланс равен: {user[4]}\nВам не хватает.")
from aiogram import Bot
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, CallbackQuery
import os
from Aiogram.games_bot.core.utils.dbconnect import Database
from Aiogram.games_bot.core.keyboards.profile_kb import balance_kb

# Оплата через бот
async def view_balance(message: Message, bot: Bot):
    db = Database(os.getenv('DATABASE'))
    user = db.select_user_id(message.from_user.id)
    await bot.send_message(message.from_user.id, f"💰 Ваш баланс: {user[4]} руб.", reply_markup=balance_kb())

async def add_balance(call: CallbackQuery):
    await call.bot.send_invoice(
        chat_id=call.from_user.id,
        title='Пополнить баланс',
        description='Пополнение баланса',
        provider_token=os.getenv("TOKEN_YOUKASSA"),
        payload="add_balance",
        currency='rub',
        prices=[
            LabeledPrice(
                label='500 р.',
                amount=50000
            )
        ],
        start_parameter='zandrex_bot',
        provider_data=None,
        need_name=False,
        need_phone_number=False,
        need_email=False,
        need_shipping_address=False,
        send_phone_number_to_provider=False,
        send_email_to_provider=False,
        is_flexible=False,
        disable_notification=False,
        protect_content=False,
        reply_to_message_id=None,
        reply_markup=None,
        request_timeout=60
    )


async def pay_pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

async def successful_payment(message: Message, bot: Bot):
    db = Database(os.getenv('DATABASE'))
    balance = db.select_user_id(message.from_user.id)
    balance = balance[4] + message.successful_payment.total_amount // 100
    db.balance_user_edit(message.from_user.id, balance)
    db.balance_system(f'+ {message.successful_payment.total_amount // 100}', message.from_user.id)
    await bot.send_message(message.from_user.id, f"Ваш баланс пополнен на "
                                                 f"{message.successful_payment.total_amount // 100}")

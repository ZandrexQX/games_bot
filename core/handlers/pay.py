from aiogram import Bot
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery
from Aiogram.base import config

# Оплата через бот
async def order(message: Message, bot: Bot):
    await bot.send_invoice(
        chat_id=message.chat.id,
        title='Покупка через бот',
        description='Учимся',
        payload='Payment',
        provider_token=config.TEST_PAYMENT,
        currency='rub',
        prices=[
            LabeledPrice(
                label='Secret',
                amount=90000
            ),
            LabeledPrice(
                label='nds',
                amount=9000
            ),
            LabeledPrice(
                label='Skidka',
                amount=-5000
            ),
            LabeledPrice(
                label='Bonus',
                amount=-10000
            )
        ],
        max_tip_amount=5000,
        suggested_tip_amounts=[1000, 2000, 3000, 4000],
        start_parameter='zandrex',
        provider_data=None,
        need_name=True,
        need_phone_number=True,
        need_email=True,
        need_shipping_address=False,
        send_phone_number_to_provider=False,
        send_email_to_provider=False,
        is_flexible=False,
        disable_notification=False,
        protect_content=False,
        reply_to_message_id=None,
        allow_sending_without_reply=True,
        reply_markup=None,
        request_timeout=15
    )


async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

async def successful_payment(message: Message):
    msg = f'Спасибо за оплату {message.successful_payment.total_amount // 100} {message.successful_payment.currency}.' \
          f'Уже обрабатываем.'
    await message.answer(msg)

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import datetime

def get_profile_kb():
    kb_builder = ReplyKeyboardBuilder()

    kb_builder.button(text='Актуальные игры')
    kb_builder.button(text='Мои игры')
    kb_builder.button(text='Баланс')
    kb_builder.button(text='История игр')
    kb_builder.adjust(2)
    return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True,
                         input_field_placeholder='Выберите действие:')

def get_date_kb():
    kb = InlineKeyboardBuilder()
    current_date = datetime.date.today()
    for i in range(7):
        current_date += datetime.timedelta(days=1)
        kb.button(text=f'{current_date.strftime("%d.%m")}', callback_data=f"view_date_{current_date.strftime('%d.%m.%y')}")
    kb.adjust(1)
    return kb.as_markup()

def add_match(game_id, user_id):
    kb = InlineKeyboardBuilder()
    kb.button(text="Записаться на матч", callback_data=f"add_match_{game_id}_{user_id}")
    kb.adjust(1)
    return kb.as_markup()

def del_match(game_id, user_id):
    kb = InlineKeyboardBuilder()
    kb.button(text="Удалить запись", callback_data=f"del_match_{game_id}_{user_id}")
    kb.adjust(1)
    return kb.as_markup()

def del_buy_match(game_id, user_id):
    kb = InlineKeyboardBuilder()
    kb.button(text='Удалить запись', callback_data=f"del_match_{game_id}_{user_id}")
    kb.button(text='Оплатить игру', callback_data=f"pay_game_{game_id}_{user_id}")
    kb.adjust(1)
    return kb.as_markup()

def balance_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="Пополнить баланс", callback_data='add_balance')
    kb.adjust(1)
    return kb.as_markup()

def add_sub(user_id):
    kb = InlineKeyboardBuilder()
    kb.button(text="Подписаться на обновления", callback_data=f'edit_sub_{user_id}')
    kb.adjust(1)
    return kb.as_markup()

def del_sub(user_id):
    kb = InlineKeyboardBuilder()
    kb.button(text="Отписаться от обновлений", callback_data=f'edit_sub_{user_id}')
    kb.adjust(1)
    return kb.as_markup()
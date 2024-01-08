from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_reg_kb():
    kb_builder = ReplyKeyboardBuilder()

    kb_builder.button(text='Зарегистрироваться')
    return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True,
                         input_field_placeholder='Нажмите на кнопку')

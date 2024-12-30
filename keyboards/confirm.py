from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def get_confirm_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text='Confirm', callback_data='Confirm')
    builder.button(text='Cancel', callback_data='Cancel')

    return builder.as_markup(resize_keyboard=True)


def get_yes_no_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text='Yes')
    builder.button(text='No')

    return builder.as_markup(resize_keyboard=True)


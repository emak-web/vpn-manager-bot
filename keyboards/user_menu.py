from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def get_main_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text='🔍 VPN Статус')
    builder.button(text='📄 Мои Конфиги')
    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)


def get_choose_config_keyboard(number_of_configs: int):
    builder = InlineKeyboardBuilder()

    for i in range(1, number_of_configs+1):
        builder.button(
            text=f'Конфиг {i}', callback_data=str(i)
        )
    
    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)
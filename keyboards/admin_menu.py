from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from services.db_connector import db
from cbdata import ChooseUserCallbackFactory

def get_main_menu():
    builder = ReplyKeyboardBuilder()

    builder.button(text='🛠 Manage Server')
    builder.button(text='🖥 Manage VPN')
    builder.button(text='👥 Manage Users')
    builder.button(text='🗂 Manage Configs')
    builder.button(text='🗣 Make an Announcement')
    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)


def get_manage_server_menu():
    builder = ReplyKeyboardBuilder()

    builder.button(text='🖥 Status')
    builder.button(text='🔄 Restart')
    builder.button(text='🏠 Main Menu')
    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)


def get_status_menu():
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Update', callback_data='status_update'
    )

    return builder.as_markup(resize_keyboard=True)


def get_manage_configs_menu():
    builder = ReplyKeyboardBuilder()

    builder.button(text='Get my Config')
    builder.button(text='Get User\'s Config')
    builder.button(text='Regenerate Everyone\'s Configs')
    builder.button(text='Create New Config')
    builder.button(text='🏠 Main Menu')
    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)


def get_manage_users_menu():
    builder = ReplyKeyboardBuilder()

    builder.button(text='📋 User List')
    builder.button(text='📋 Wait List')
    builder.button(text='Add to Wait List')
    builder.button(text='Remove from Wait List')
    builder.button(text='🏠 Main Menu')
    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)


def get_manage_vpn_menu():
    builder = ReplyKeyboardBuilder()

    builder.button(text='🖥 VPN Status')
    builder.button(text='👥 Show Peers')
    builder.button(text='🔄 Restart Wireguard')
    builder.button(text='🏠 Main Menu')
    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)


def get_choose_user_keyboard():
    users = db.get_fillname_list()
    builder = InlineKeyboardBuilder()

    for user in users:
        builder.button(
            text=str(user[0]), callback_data=ChooseUserCallbackFactory(user_id=user[1], fullname=user[0])
        )
    
    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)


def get_choose_user_from_waitlist_inlinekeyboard(users):
    builder = InlineKeyboardBuilder()

    for user in users:
        builder.button(
            text=str(user), callback_data=str(user)
        )
    
    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)


def get_choose_config_keyboard(number_of_configs: int):
    builder = InlineKeyboardBuilder()

    for i in range(1, number_of_configs+1):
        builder.button(
            text=f'Config {i}', callback_data=str(i)
        )
    
    builder.adjust(1)
    
    return builder.as_markup(resize_keyboard=True)
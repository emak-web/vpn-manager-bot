from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from commands.admin_commands import AdminCommands

def get_main_menu():
    builder = ReplyKeyboardBuilder()

    builder.button(text=AdminCommands.MANAGE_PEERS)
    builder.button(text=AdminCommands.MANAGE_WG)
    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)


def get_manage_peers_menu():
    builder = ReplyKeyboardBuilder()

    builder.button(text=AdminCommands.CREATE_PEER)
    builder.button(text=AdminCommands.DELETE_PEER)
    builder.button(text=AdminCommands.SHOW_PEERS)
    builder.button(text=AdminCommands.GENERATE_CONFIG)
    builder.button(text=AdminCommands.MAIN_MENU)
    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)


def get_confirm_menu():
    builder = ReplyKeyboardBuilder()

    builder.button(text=AdminCommands.CONFIRM)
    builder.button(text=AdminCommands.CANCEL)
    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)


def get_choose_peer_inline_keyboard(peers):
    builder = InlineKeyboardBuilder()

    for peer in peers:
        if  peer[0]:
            builder.button(
                text=f'{peer[0]} {peer[1]}', callback_data=f'{peer[0]}'
            )
    
    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)


def get_manage_wg_menu():
    builder = ReplyKeyboardBuilder()

    builder.button(text=AdminCommands.START_WG)
    builder.button(text=AdminCommands.STOP_WG)
    builder.button(text=AdminCommands.RESTART_WG)
    builder.button(text=AdminCommands.STATUS_WG)
    builder.button(text=AdminCommands.SHOW_CONNECTIONS_WG)
    builder.button(text=AdminCommands.MAIN_MENU)
    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)


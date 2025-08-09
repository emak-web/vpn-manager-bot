from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from filters import is_admin
from keyboards import admin_menu
from messages.admin_messages import AdminMessages
from commands.admin_commands import AdminCommands


router = Router()
router.message.filter(is_admin.IsAdminFilter())
router.callback_query.filter(is_admin.IsAdminFilter())


@router.message(Command('start'))
async def start(message: Message):
    # TODO update db
    await message.answer(
        AdminMessages.WELCOME,
        reply_markup=admin_menu.get_main_menu()
    )


@router.message(F.text == AdminCommands.MAIN_MENU)
async def main_menu(message: Message):
    await message.answer(
        AdminMessages.MAIN_MENU,
        reply_markup=admin_menu.get_main_menu()
    )

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from filters import is_admin
from keyboards import admin_menu
from services.db_connector import db


router = Router()
router.message.filter(is_admin.IsAdminFilter(is_admin=True))
router.callback_query.filter(is_admin.IsAdminFilter(is_admin=True))


@router.message(Command('start'))
async def cmd_start(message: Message):
    db.update_user_data(
        message.from_user.id,
        message.from_user.username,
        message.from_user.full_name
    )
    await message.answer(
        '<b>Hello Admin!</b>',
        reply_markup=admin_menu.get_main_menu()
    )


@router.message(F.text == '🏠 Main Menu')
async def cmd_start(message: Message):
    await message.answer(
        '✅ Main Menu',
        reply_markup=admin_menu.get_main_menu()
    )

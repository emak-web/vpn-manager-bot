from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, BufferedInputFile
from aiogram.fsm.context import FSMContext


from filters import is_admin
from keyboards import admin_menu
from messages.admin_messages import AdminMessages
from commands.admin_commands import AdminCommands
from utils.wg import WireGuard


router = Router()
router.message.filter(is_admin.IsAdminFilter())
router.callback_query.filter(is_admin.IsAdminFilter())


@router.message(F.text == AdminCommands.MANAGE_WG)
async def manage_wg_menu(message: Message):
    await message.answer(
        AdminMessages.MANAGE_WG,
        reply_markup=admin_menu.get_manage_wg_menu()
    )


@router.message(F.text == AdminCommands.START_WG)
async def start_wg(message: Message):
    wg = WireGuard()
    wg.start()
    await message.answer(
        AdminMessages.DONE,
        reply_markup=admin_menu.get_manage_wg_menu()
    )

@router.message(F.text == AdminCommands.STOP_WG)
async def stop_wg(message: Message):
    wg = WireGuard()
    wg.stop()
    await message.answer(
        AdminMessages.DONE,
        reply_markup=admin_menu.get_manage_wg_menu()
    )


@router.message(F.text == AdminCommands.RESTART_WG)
async def restart_wg(message: Message):
    wg = WireGuard()
    wg.restart()
    await message.answer(
        AdminMessages.DONE,
        reply_markup=admin_menu.get_manage_wg_menu()
    )


@router.message(F.text == AdminCommands.STATUS_WG)
async def status_wg(message: Message):
    wg = WireGuard()
    await message.answer(
        wg.status(),
        reply_markup=admin_menu.get_manage_wg_menu()
    )


@router.message(F.text == AdminCommands.SHOW_CONNECTIONS_WG)
async def show_connections_wg(message: Message):
    wg = WireGuard()
    await message.answer(
        wg.show_connections(),
        reply_markup=admin_menu.get_manage_wg_menu()
    )
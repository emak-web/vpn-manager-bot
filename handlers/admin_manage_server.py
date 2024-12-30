from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from filters import is_admin
from forms import admin_forms
from keyboards import admin_menu, confirm
from services import server_actions


router = Router()
router.message.filter(is_admin.IsAdminFilter(is_admin=True))
router.callback_query.filter(is_admin.IsAdminFilter(is_admin=True))


@router.message(F.text == '🛠 Manage Server')
async def cmd_manage_server(message: Message):
    await message.answer(
        '✅ Manage Server Menu',
        reply_markup=admin_menu.get_manage_server_menu()
    )


@router.message(F.text == '🖥 Status')
async def cmd_status(message: Message):
    status = server_actions.get_server_status()
    await message.answer(
        f'<b>Current server status</b>\n{status}',
        reply_markup=admin_menu.get_status_menu()
    )


@router.callback_query(F.data == 'status_update')
async def call_back_status_update(callback: CallbackQuery):
    status = server_actions.get_server_status()
    await callback.message.edit_text(
        f'<b>Current server status</b>\n{status}',
        reply_markup=admin_menu.get_status_menu()
    )


@router.message(F.text == '🔄 Restart')
async def cmd_restart(message: Message, state: FSMContext):
    await state.set_state(admin_forms.RestartServer.confirm)
    await message.answer(
        'Confirm server restart',
        reply_markup=confirm.get_confirm_keyboard()
    )


@router.callback_query(admin_forms.RestartServer.confirm)
async def call_back_restart_server(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
            callback.message.text,
            reply_markup=None
        )
    await state.clear()

    if callback.data == 'Confirm':
        answer = '✅ Done'
        await callback.message.answer(
            answer,
            reply_markup=admin_menu.get_main_menu()
        )
        server_actions.restart_server()
    elif callback.data == 'Cancel':
        answer = '❌ Canceled'
        await callback.message.answer(
            answer,
            reply_markup=admin_menu.get_manage_server_menu()
        )

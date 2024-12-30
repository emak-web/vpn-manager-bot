from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from filters import is_admin
from forms import admin_forms
from keyboards import admin_menu, confirm
from services import wireguard_actions


router = Router()
router.message.filter(is_admin.IsAdminFilter(is_admin=True))
router.callback_query.filter(is_admin.IsAdminFilter(is_admin=True))


@router.message(F.text == '🖥 Manage VPN')
async def cmd_manage_vpn(message: Message):
    await message.answer(
        '✅ Manage VPN Menu',
        reply_markup=admin_menu.get_manage_vpn_menu()
    )


@router.message(F.text == '🖥 VPN Status')
async def cmd_vpn_status(message: Message):
    await message.answer(
        wireguard_actions.get_peer(message.from_user.full_name, message.from_user.username),
        reply_markup=admin_menu.get_manage_vpn_menu()
    )


@router.message(F.text == '👥 Show Peers')
async def cmd_show_peers(message: Message):
    await message.answer(
        wireguard_actions.get_peers(),
        reply_markup=admin_menu.get_manage_vpn_menu()
    )


@router.message(F.text == '🔄 Restart Wireguard')
async def cmd_restart_wireguard(message: Message, state: FSMContext):
    await state.set_state(admin_forms.RestartWireguard.confirm)
    await message.answer(
        'Confirm WireGuard restart',
        reply_markup=confirm.get_confirm_keyboard()
    )


@router.callback_query(admin_forms.RestartWireguard.confirm)
async def call_back_restart_wireguard(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'Confirm':
        wireguard_actions.restart_wireguard()
        answer = '✅ Done'
    elif callback.data == 'Cancel':
        answer = '❌ Canceled'

    await callback.message.edit_text(
            callback.message.text,
            reply_markup=None
        )
    await callback.message.answer(
            answer,
            reply_markup=admin_menu.get_manage_vpn_menu()
        )
    await state.clear()

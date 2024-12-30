from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from filters import is_admin
from forms import admin_forms
from keyboards import admin_menu, confirm
from services import message_actions


router = Router()
router.message.filter(is_admin.IsAdminFilter(is_admin=True))
router.callback_query.filter(is_admin.IsAdminFilter(is_admin=True))


@router.message(F.text == '🗣 Make an Announcement')
async def cmd_make_announcement(message: Message, state: FSMContext):
    await state.set_state(admin_forms.Anouncement.announcement)
    await message.answer(
        'Send a message for the announcement',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(admin_forms.Anouncement.announcement)
async def handle_announcement(message: Message, state: FSMContext):
    await state.update_data(anouncement=message.text)
    await state.set_state(admin_forms.Anouncement.confirm)
    await message.answer(
        f'<b>Your announcement:</b>\n\n{message.text}',
        reply_markup=confirm.get_confirm_keyboard()
    )


@router.callback_query(admin_forms.Anouncement.confirm)
async def call_back_status_update(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    announcement = data['anouncement']
    
    if callback.data == 'Confirm':
        answer = '✅ Announcement sent'
        await message_actions.notify_users(callback.message.bot, announcement)

    elif callback.data == 'Cancel':
        answer = '❌ Announcement cenceled'

    await callback.message.edit_text(
        callback.message.text,
        reply_markup=None
    )
    await callback.message.answer(
        answer,
        reply_markup=admin_menu.get_main_menu()
    )
    await state.clear()

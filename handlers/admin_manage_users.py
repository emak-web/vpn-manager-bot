from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext


from filters import is_admin
from forms import admin_forms
from keyboards import admin_menu, confirm
from services.db_connector import db


router = Router()
router.message.filter(is_admin.IsAdminFilter(is_admin=True))
router.callback_query.filter(is_admin.IsAdminFilter(is_admin=True))


@router.message(F.text == '👥 Manage Users')
async def cmd_manage_bot_users(message: Message):
    await message.answer(
        '✅ Manage Users Menu',
        reply_markup=admin_menu.get_manage_users_menu()
    )


@router.message(F.text == 'Add to Wait List')
async def cmd_add_user(message: Message, state: FSMContext):
    await state.set_state(admin_forms.AddUser.username)
    await message.answer(
        'Type their username',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(admin_forms.AddUser.username)
async def handle_username(message: Message, state: FSMContext):
    username = message.text
    await state.update_data(username=username)
    await state.set_state(admin_forms.AddUser.confirm)
    await message.answer(
        f'Add @{username} to waitlist?',
        reply_markup=confirm.get_confirm_keyboard()
    )


@router.callback_query(admin_forms.AddUser.confirm)
async def call_back_confirm(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    if callback.data == 'Confirm':
        db.add_user(data['username'])
        answer = '✅ Done'
    elif callback.data == 'Cancel':
        answer = '❌ Canceled'

    await callback.message.edit_text(
            callback.message.text,
            reply_markup=None
        )
    await callback.message.answer(
            answer,
            reply_markup=admin_menu.get_manage_users_menu()
        )
    await state.clear()


@router.message(F.text == 'Remove from Wait List')
async def cmd_remove_user_from_waitlist(message: Message, state: FSMContext):
    waitlist = db.get_wait_list()
    if waitlist:
        await state.set_state(admin_forms.RemoveUser.username)
        await message.answer(
            'Choose user',
            reply_markup=admin_menu.get_choose_user_from_waitlist_inlinekeyboard(waitlist)
        )
    else:
        await message.answer(
            'Wait list is empty.',
            reply_markup=admin_menu.get_manage_users_menu()
        )


@router.callback_query(admin_forms.RemoveUser.username)
async def handle_username(callback: CallbackQuery, state: FSMContext):
    username = callback.data
    await callback.message.edit_text(
        f'Remove @{username} from wait list?',
        reply_markup=confirm.get_confirm_keyboard()
    )
    await state.update_data(username=username)
    await state.set_state(admin_forms.RemoveUser.confirm)
    

@router.callback_query(admin_forms.RemoveUser.confirm)
async def call_back_status_update(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    if callback.data == 'Confirm':
        db.remove_from_wait_list(data['username'])
        answer = '✅ Done'
    elif callback.data == 'Cancel':
        answer = '❌ Canceled'

    await callback.message.edit_text(
            callback.message.text,
            reply_markup=None
        )
    await callback.message.answer(
            answer,
            reply_markup=admin_menu.get_manage_users_menu()
        )
    await state.clear()


@router.message(F.text == '📋 User List')
async def cmd_get_user_list(message: Message):
    users = db.get_user_list()

    result = '📋 User List:\n\n'
    
    for user in users:
        user_id = user[1]
        username = user[2]
        fullname = user[3]
        number_of_configs = db.get_number_of_configs(user_id)

        result += f'Fullname: <b>{fullname}</b>\nUsername: @{username}\nUser ID: {user_id}\nNumber of configs: {number_of_configs}\n\n'
    
    await message.answer(
        result,
        reply_markup=admin_menu.get_manage_users_menu()
    )


@router.message(F.text == '📋 Wait List')
async def cmd_get_user_list(message: Message):
    waitlist = db.get_wait_list()

    if len(waitlist) == 0:
        result = 'Wait list is empty'
    else:
        result = '📋 Wait List:\n'

        for user in waitlist:
            result += f'@{user}\n'
    
    await message.answer(
        result,
        reply_markup=admin_menu.get_manage_users_menu()
    )

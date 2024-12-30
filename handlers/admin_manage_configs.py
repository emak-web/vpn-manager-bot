from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from filters import is_admin
from forms import admin_forms
from keyboards import admin_menu, confirm
from services import message_actions
from services.db_connector import db
from cbdata import ChooseUserCallbackFactory


router = Router()
router.message.filter(is_admin.IsAdminFilter(is_admin=True))
router.callback_query.filter(is_admin.IsAdminFilter(is_admin=True))


@router.message(F.text == '🗂 Manage Configs')
async def cmd_manage_wg_configs(message: Message):
    await message.answer(
        '✅ Manage WG Configs Menu',
        reply_markup=admin_menu.get_manage_configs_menu()
    )


@router.message(F.text == 'Get my Config')
async def cmd_get_my_config(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_configs = db.get_user_configs(user_id)
    number_of_configs = len(user_configs)

    # if user has no configs
    if number_of_configs == 0:
        await message.answer('You have no configs')
        await state.clear()

    elif number_of_configs == 1:
        await message_actions.send_or_create_config_file(
            message, user_id, user_configs, 0, 'Your wg config', admin_menu.get_manage_configs_menu()
        )
        await state.clear()
            
    elif number_of_configs > 1:
        await state.set_state(admin_forms.GetConfig.index)
        await state.update_data(user_id=user_id, configs=user_configs)
        await message.answer(
            'Choose config',
            reply_markup=admin_menu.get_choose_config_keyboard(number_of_configs)
        )


@router.callback_query(admin_forms.GetConfig.index)
async def get_config_index(callback: CallbackQuery, state: FSMContext):
    index = int(callback.data) - 1
    data = await state.get_data()
    user_configs = data['configs']
    user_id = data['user_id']

    await message_actions.send_or_create_config_file(
        callback.message, user_id, user_configs, index, 'Your wg config', admin_menu.get_manage_configs_menu()
    )

    await callback.message.delete()
    await state.clear()


@router.message(F.text == 'Get User\'s Config')
async def cmd_get_users_config(message: Message, state: FSMContext):
    await state.set_state(admin_forms.GetUsersConfig.user)
    await message.answer(
        'Choose user',
        reply_markup=admin_menu.get_choose_user_keyboard()
    )


@router.callback_query(admin_forms.GetUsersConfig.user, ChooseUserCallbackFactory.filter())
async def get_user_callback(callback: CallbackQuery, state: FSMContext, callback_data: ChooseUserCallbackFactory):
    await callback.message.delete()

    user_id = callback_data.user_id
    fullname = callback_data.fullname
    user_configs = db.get_user_configs(user_id)
    number_of_configs = len(user_configs)

    # if user has no configs
    if number_of_configs == 0:
        await callback.message.answer(f'{fullname} has no configs')
        await state.clear()

    elif number_of_configs == 1:
        await message_actions.send_or_create_config_file(
            callback.message, user_id, user_configs, 0, 'User config', admin_menu.get_manage_configs_menu()
        )
        await state.clear()
            
    elif number_of_configs > 1:
        await state.set_state(admin_forms.GetUsersConfig.index)
        await state.update_data(user_id=user_id, configs=user_configs, fullname=fullname)
        await callback.message.answer(
            'Choose config',
            reply_markup=admin_menu.get_choose_config_keyboard(number_of_configs)
        )
    

@router.callback_query(admin_forms.GetUsersConfig.index)
async def get_config_index(callback: CallbackQuery, state: FSMContext):
    index = int(callback.data) - 1
    data = await state.get_data()
    user_configs = data['configs']
    user_id = data['user_id']
    fullname = data['fullname']

    await message_actions.send_or_create_config_file(
        callback.message, user_id, user_configs, index, 'User config', admin_menu.get_manage_configs_menu()
    )
    
    await callback.message.delete()
    await state.clear()


@router.message(F.text == 'Regenerate Everyone\'s Configs')
async def cmd_regenerate_everyones_configs(message: Message, state: FSMContext):
    await state.set_state(admin_forms.RegenerateConfigs.confirm)
    await message.answer(
        'Are you sure you want to regenerate all configs?',
        reply_markup=confirm.get_confirm_keyboard()
    )


@router.callback_query(admin_forms.RegenerateConfigs.confirm)
async def call_back_regenerate_everyones_configs(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
            callback.message.text,
            reply_markup=None
        )
    await state.clear()

    if callback.data == 'Confirm':
        answer = '✅ Done'
        db.remove_all_file_ids()
        
    elif callback.data == 'Cancel':
        answer = '❌ Canceled'
    
    await callback.message.answer(
        answer,
        reply_markup=admin_menu.get_manage_configs_menu()
    )


# @router.message(F.text == 'Create New Config')
# async def cmd_create_new_config(message: Message, state: FSMContext):
#     await state.set_state(admin_forms.CreateNewConfig.user)
#     await message.answer(
#         'Choose who to associate the new config with',
#         reply_markup=admin_menu.get_choose_user_keyboard()
#     )


# @router.callback_query(admin_forms.CreateNewConfig.user, ChooseUserCallbackFactory.filter())
# async def cmd_create_new_config_get_user(
#     callback: CallbackQuery,
#     state: FSMContext,
#     callback_data: ChooseUserCallbackFactory
#     ):
#     user_id = callback_data.user_id
#     await callback.message.delete()
#     await state.clear()
#     # if message.text in fullnames:
#     #     user_id = config_actions.find_user_by_fullname(message.text)
#     #     config_actions.generate_keys(user_id)
#     #     config_text = config_actions.add_new_peer(user_id)

#     #     await message.answer(
#     #         f'Linking config to user: {user_id}, generating keys...',
#     #     )
#     #     await message.answer(
#     #         f'Modifing wg0.conf...\n\n{config_text}',
#     #     )
#     #     await message.answer(
#     #         'Do you want to restart wireguard?',
#     #         reply_markup=confirm.get_yes_no_keyboard()
#     #     )
#     #     await state.set_state(CreateNewConfig.restart_server)
#     # else:
#     #     await message.answer(
#     #         'No user with such name, try again',
#     #         reply_markup=admin_menu.get_choose_user_keyboard()
#     #     )


# @router.message(admin_forms.CreateNewConfig.restart_server)
# async def cmd_create_new_config(message: Message, state: FSMContext):
#     if message.text == 'Yes':
#         print('restarting wg...')
#     elif message.text == 'No':
#         print('restarting wg...')
    
#     if message.text == 'Yes' or message.text == 'No':
#         await message.answer(
#             '✅ Done',
#             reply_markup=admin_menu.get_manage_configs_menu()
#         )
#         await state.clear()
#     else:
#         await message.answer(
#             'Yes/No',
#             reply_markup=confirm.get_yes_no_keyboard()
#         )


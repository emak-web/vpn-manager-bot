from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types.link_preview_options import LinkPreviewOptions

from keyboards import user_menu
from forms import user_forms
from filters import is_authorized_user
from services import message_actions, wireguard_actions
from services.db_connector import db


router = Router()
router.message.filter(is_authorized_user.IsAuthorizedUserFilter(is_user=True))
router.callback_query.filter(is_authorized_user.IsAuthorizedUserFilter(is_user=True))


@router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer(
        f'👋 Привет, {message.from_user.first_name}!\n\n🤖 Для чего нужен этот бот?\n\nПользователей моего впн с каждым днем становится все больше и больше (скорее с каждым годом), следовательно конфигов тоже становится больше и для того, чтобы упростить процесс их рассылки и возможных изменений я создал этого бота.\n\nТеперь все ваши конфиги хранятся здесь. Также можно узнать статус соединения и в некоторых случаях я буду присылать сюда объявления (по типу “впн не работает скоро все починю”).\n\nПриятного пользования!\nКнопки снизу 👇👇👇',
        reply_markup=user_menu.get_main_menu()
    )


@router.message(F.text == '🔍 VPN Статус')
async def cmd_get_status(message: Message):
    if db.get_number_of_configs(message.from_user.id):
        answer = wireguard_actions.get_peer(message.from_user.full_name, message.from_user.username)
    else:
        answer = 'У вас нет конфигов. '
    await message.answer(
        answer,
        reply_markup=user_menu.get_main_menu()
    )


@router.message(F.text == '📄 Мои Конфиги')
async def cmd_get_my_config(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_configs = db.get_user_configs(user_id)
    number_of_configs = len(user_configs)

    # if user has no configs
    if number_of_configs == 0:
        await message.answer('У вас нет конфигов.')
        await state.clear()

    # if user has one config
    elif number_of_configs == 1:
        await message_actions.send_or_create_config_file(
            message, user_id, user_configs, 0, 'Ваш WireGuard конфиг.', user_menu.get_main_menu()
        )
        await state.clear()
            
    elif number_of_configs > 1:
        await state.set_state(user_forms.GetConfig.index)
        await state.update_data(user_id=user_id, configs=user_configs)
        await message.answer(
            f'У вас есть {number_of_configs} конфига.\nВыберите какой отправить:',
            reply_markup=user_menu.get_choose_config_keyboard(number_of_configs)
        )


@router.callback_query(user_forms.GetConfig.index)
async def get_config_index(callback: CallbackQuery, state: FSMContext):
    index = int(callback.data) - 1
    data = await state.get_data()
    user_configs = data['configs']
    user_id = data['user_id']

    await callback.message.delete()
    await message_actions.send_or_create_config_file(
        callback.message, user_id, user_configs, index, 'Ваш WireGuard конфиг.', user_menu.get_main_menu()
    )
    await state.clear()

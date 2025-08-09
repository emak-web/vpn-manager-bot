import io
import qrcode
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, BufferedInputFile
from aiogram.fsm.context import FSMContext


from filters import is_admin
from keyboards import admin_menu
from forms.admin_forms import CreatePeer, GenerateConfig, DeletePeer
from messages.admin_messages import AdminMessages
from commands.admin_commands import AdminCommands
from utils.wg_config import WireGuardConfig


router = Router()
router.message.filter(is_admin.IsAdminFilter())
router.callback_query.filter(is_admin.IsAdminFilter())


@router.message(F.text == AdminCommands.MANAGE_PEERS)
async def manage_peers_menu(message: Message):
    await message.answer(
        AdminMessages.MANAGE_PEERS,
        reply_markup=admin_menu.get_manage_peers_menu()
    )


@router.message(F.text == AdminCommands.CREATE_PEER)
async def create_peer(message: Message, state: FSMContext):
    await state.set_state(CreatePeer.name)
    await message.answer(
        AdminMessages.CREATE_PEER_NAME,
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(CreatePeer.name)
async def create_peer_name(message: Message, state: FSMContext):
    # check if exists 
    await state.update_data(name=message.text)
    await state.set_state(CreatePeer.tg_username)
    await message.answer(AdminMessages.CREATE_PEER_TG_USERNAME)


@router.message(CreatePeer.tg_username)
async def create_peer_tg_username(message: Message, state: FSMContext):
    await state.update_data(tg_username=message.text)
    await state.set_state(CreatePeer.confirm)
    await message.answer(
        AdminMessages.CREATE_PEER_CONFIRM,
        reply_markup=admin_menu.get_confirm_menu()
    )


@router.message(CreatePeer.confirm)
async def create_peer_confirm(message: Message, state: FSMContext):
    if message.text == AdminCommands.CONFIRM:
        data = await state.get_data()
        wg = WireGuardConfig()
        wg.create_peer(data['name'], data['tg_username'])
        await message.answer(
            AdminMessages.DONE,
            reply_markup=admin_menu.get_manage_peers_menu()
        )
    else:
        await message.answer(
            AdminMessages.CANCELED,
            reply_markup=admin_menu.get_manage_peers_menu()
        )
    await state.clear()


@router.message(F.text == AdminCommands.GENERATE_CONFIG)
async def generate_config(message: Message, state: FSMContext):
    wg = WireGuardConfig()
    await state.set_state(GenerateConfig.name)
    await message.answer(
        AdminMessages.CHOSE_PEER,
        reply_markup=admin_menu.get_choose_peer_inline_keyboard(wg.get_peers())
    )


@router.callback_query(GenerateConfig.name)
async def generate_config_name(callback: CallbackQuery, state: FSMContext):
    wg = WireGuardConfig()
    name = callback.data

    config_str = wg.generate_config_by_name(name)

    img = qrcode.make(config_str)
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    qrcode_config = BufferedInputFile(buffer.read(), filename=f'{name}.png')

    file_bytes = io.BytesIO(config_str.encode('utf-8'))
    config = BufferedInputFile(file_bytes.read(), filename=f'{name}.conf')

    await callback.message.answer_photo(qrcode_config)
    await callback.message.answer_document(config)
    await callback.message.delete()
    await state.clear()


@router.message(F.text == AdminCommands.DELETE_PEER)
async def delete_peer(message: Message, state: FSMContext):
    wg = WireGuardConfig()
    await state.set_state(DeletePeer.name)
    await message.answer(
        AdminMessages.CHOSE_PEER,
        reply_markup=admin_menu.get_choose_peer_inline_keyboard(wg.get_peers())
    )


@router.callback_query(DeletePeer.name)
async def delete_peer_name(callback: CallbackQuery, state: FSMContext):
    await state.update_data(name=callback.data)
    await state.set_state(DeletePeer.confirm)
    await callback.message.delete()
    # TODO add name
    await callback.message.answer(
        AdminMessages.DELETE_PEER_CONFIRM,
        reply_markup=admin_menu.get_confirm_menu()
    )


@router.message(DeletePeer.confirm)
async def delete_peer_confirm(message: Message, state: FSMContext):
    if message.text == AdminCommands.CONFIRM:
        data = await state.get_data()
        wg = WireGuardConfig()
        wg.delete_peer(data['name'])
        await message.answer(
            AdminMessages.DONE,
            reply_markup=admin_menu.get_manage_peers_menu()
        )
    else:
        await message.answer(
            AdminMessages.CANCELED,
            reply_markup=admin_menu.get_manage_peers_menu()
        )
    await state.clear()
    

@router.message(F.text == AdminCommands.SHOW_PEERS)
async def show_peers(message: Message):
    wg = WireGuardConfig()

    await message.answer(
        wg.show_peers(),
        reply_markup=admin_menu.get_manage_peers_menu()
    )
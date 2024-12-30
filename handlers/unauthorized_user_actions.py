from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from services.db_connector import db
from services import message_actions
from keyboards import user_menu


router = Router()


@router.message(Command('start'))
async def cmd_start(message: Message):
    if message.from_user.username in db.get_wait_list():
        db.add_user_from_wait_list(
            message.from_user.id,
            message.from_user.username,
            message.from_user.full_name
        )
        await message.answer(
            f'👋 Привет, {message.from_user.first_name}!\n\n🤖 Для чего нужен этот бот?\n\nПользователей моего впн с каждым днем становится все больше и больше (скорее с каждым годом), следовательно конфигов тоже становится больше и для того, чтобы упростить процесс их рассылки и возможных изменений я создал этого бота.\n\nТеперь все ваши конфиги хранятся здесь. Также можно узнать статус соединения и в некоторых случаях я буду присылать сюда объявления (по типу “впн не работает скоро все починю”).\n\nПриятного пользования!\nКнопки снизу 👇👇👇',
            reply_markup=user_menu.get_main_menu()
        )
        await message_actions.notify_admins(
            message.bot,
            f'@{message.from_user.username} has been added from the wait list'
        )
    else:
        await message.answer(
            'Я тебя не знаю.'
        )

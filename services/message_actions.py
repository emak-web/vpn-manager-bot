from aiogram.types import FSInputFile
from config_reader import config
from services import config_actions
from services.db_connector import db


async def notify_admins(bot, message):
    admins = config.admins

    for admin in admins:
        await bot.send_message(admin, '🔔 '+message)


async def notify_users(bot, message):
    users = db.get_user_id_list()
    admins = config.admins

    for user in users:
        if user not in admins:
            await bot.send_message(user, '🔔 '+message)


async def send_or_create_config_file(message, user_id, user_configs, index, caption, reply_markup):
    file_id = user_configs[index]['file_id']

    if file_id:
        await message.answer_document(
            document=file_id,
            caption=caption,
            reply_markup=reply_markup
        )
    else:
        username = db.get_username(user_id)
        file_name = config_actions.generate_config(
                user_configs[index]['privatekey'],
                user_configs[index]['ip'],
                username,
                index
            )
        file = FSInputFile(f'wg_configs/{file_name}')
        result = await message.answer_document(
            file,
            caption=caption,
            reply_markup=reply_markup
        )
        db.add_file_id(user_configs[index]['id'], result.document.file_id)

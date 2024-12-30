import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config_reader import config
from handlers import (
    admin_actions, 
    admin_manage_server,
    admin_manage_vpn,
    admin_manage_users,
    admin_manage_configs,
    admin_make_announcement, 
    unauthorized_user_actions,
    user_actions
)


async def main():
    bot = Bot(
        token=config.bot_token.get_secret_value(),
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )
    dp = Dispatcher()
    dp.message.filter(F.chat.type == "private")

    dp.include_router(admin_actions.router)
    dp.include_router(admin_manage_server.router)
    dp.include_router(admin_manage_vpn.router)
    dp.include_router(admin_manage_users.router)
    dp.include_router(admin_manage_configs.router)
    dp.include_router(admin_make_announcement.router)
    dp.include_router(user_actions.router)
    dp.include_router(unauthorized_user_actions.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

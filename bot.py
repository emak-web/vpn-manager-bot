import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config.config import env
from handlers import (
    admin_actions, 
    admin_manage_peers,
    admin_manage_wireguard
)


async def main():
    bot = Bot(
        token=env.bot_token.get_secret_value(),
        default=DefaultBotProperties(
            parse_mode=ParseMode.MARKDOWN
        )
    )
    dp = Dispatcher()
    dp.message.filter(F.chat.type == "private")

    dp.include_router(admin_actions.router)
    dp.include_router(admin_manage_peers.router)
    dp.include_router(admin_manage_wireguard.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

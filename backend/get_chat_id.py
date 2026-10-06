from telegram import Bot
from config.settings import TELEGRAM_TOKEN
import asyncio


async def main():

    bot = Bot(TELEGRAM_TOKEN)

    updates = await bot.get_updates()

    if not updates:
        print("هیچ پیامی پیدا نشد. اول در تلگرام /start بزن.")
        return


    for u in updates:

        if u.message:

            print("CHAT ID:", u.message.chat.id)



asyncio.run(main())

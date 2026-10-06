from telegram import Bot
from config.settings import TELEGRAM_TOKEN, CHAT_ID
from core.report import generate_report
import asyncio


async def send_report():

    bot = Bot(
        TELEGRAM_TOKEN
    )


    text = generate_report()


    await bot.send_message(

        chat_id=CHAT_ID,

        text=text

    )


    print(
        "AURA report sent"
    )



if __name__ == "__main__":

    asyncio.run(
        send_report()
    )

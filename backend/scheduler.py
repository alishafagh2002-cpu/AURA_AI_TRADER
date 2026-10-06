
import asyncio
from core.alert_engine import alert_report
from core.history import save_signal
from telegram import Bot
from config.settings import TELEGRAM_TOKEN, CHAT_ID


bot = Bot(TELEGRAM_TOKEN)


async def send_alert():

    alert = alert_report()

    if not alert:
        return

    if "WATCH" in alert:

        await bot.send_message(
            chat_id=CHAT_ID,
            text=alert
        )

        save_signal(alert)



async def run():

    while True:

        try:
            await send_alert()

        except Exception as e:
            print(e)


        await asyncio.sleep(900)



if __name__ == "__main__":

    asyncio.run(run())

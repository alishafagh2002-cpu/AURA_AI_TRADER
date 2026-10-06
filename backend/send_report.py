from telegram import Bot
from config.settings import TELEGRAM_TOKEN, CHAT_ID
from core.market import get_market
from core.analysis import analyze
import asyncio


async def send_report():

    bot = Bot(TELEGRAM_TOKEN)

    data = get_market()

    result = analyze(data)


    best = result["🏆 بهترین فرصت"][0]


    text = f"""
🤖 AURA گزارش بازار

🏆 بهترین فرصت:

{best["نام"]}
({best["نماد"]})

💵 قیمت:
{best["قیمت"]} دلار

📈 تغییر ۲۴ ساعت:
{best["تغییر ۲۴ ساعت"]}٪

🧠 امتیاز:
{best["امتیاز AURA"]}

📌 وضعیت:
{best["تصمیم"]}

⚠️ تحلیل الگوریتمی است و تضمین سود ندارد.
"""


    await bot.send_message(
        chat_id=CHAT_ID,
        text=text
    )


if __name__ == "__main__":

    asyncio.run(send_report())

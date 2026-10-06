from telegram import Bot
from config.settings import TELEGRAM_TOKEN
from core.market import get_market
from core.analysis import analyze
import asyncio


CHAT_ID = "اینجا بعداً Chat ID تو قرار می‌گیرد"


async def send_report():

    bot = Bot(TELEGRAM_TOKEN)

    data = get_market()

    result = analyze(data)


    best = result["🏆 بهترین فرصت"][0]


    message = f"""
🤖 AURA گزارش بازار

🏆 بهترین فرصت:

{best["نام"]}

نماد:
{best["نماد"]}

قیمت:
{best["قیمت"]} دلار

تغییر ۲۴ ساعت:
{best["تغییر ۲۴ ساعت"]}٪

امتیاز:
{best["امتیاز AURA"]}

وضعیت:
{best["تصمیم"]}

⚠️ تحلیل الگوریتمی است
"""


    await bot.send_message(
        chat_id=CHAT_ID,
        text=message
    )


if __name__ == "__main__":

    asyncio.run(send_report())

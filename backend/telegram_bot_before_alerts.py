# -*- coding: utf-8 -*-

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from config.settings import TELEGRAM_TOKEN
from core.report import generate_report, get_data
from datetime import datetime


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        """
AURA AI Trader

دستیار تحلیل هوشمند بازار فعال شد.

دستورات:

/report
گزارش کامل بازار

/top
فرصت‌های برتر AURA

/status
وضعیت سیستم

/id
نمایش Chat ID
"""
    )


async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        f"Chat ID شما:\n{update.message.chat.id}"
    )


async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        await update.message.reply_text(
            generate_report()
        )

    except Exception as e:
        await update.message.reply_text(
            f"Report Error:\n{e}"
        )


async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        data = get_data()

        if not data:

            await update.message.reply_text(
                "AURA: سیگنالی پیدا نشد"
            )

            return


        text = "AURA TOP SIGNALS\n\n"


        for i, coin in enumerate(data[:5], 1):

            text += f"""
Rank {i}

{coin["نام"]} ({coin["نماد"]})

Score:
{coin["امتیاز AURA"]}

Decision:
{coin["تصمیم"]}

----------------------

"""


        await update.message.reply_text(text)


    except Exception as e:

        await update.message.reply_text(
            f"Error:\n{e}"
        )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        data = get_data()

        await update.message.reply_text(
            f"""
AURA STATUS

Bot:
Online

Market Engine:
OK

Technical Engine:
OK

Signals:
{len(data)}

Time:
{datetime.now().strftime("%Y-%m-%d %H:%M")}
"""
        )

    except Exception as e:

        await update.message.reply_text(
            f"Status Error:\n{e}"
        )


def run():

    app = Application.builder().token(
        TELEGRAM_TOKEN
    ).build()


    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("id", get_id))
    app.add_handler(CommandHandler("report", report))
    app.add_handler(CommandHandler("top", top))
    app.add_handler(CommandHandler("status", status))


    print("AURA Bot Running")

    app.run_polling()


if __name__ == "__main__":
    run()


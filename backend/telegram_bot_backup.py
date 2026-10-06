from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

from config.settings import TELEGRAM_TOKEN
from core.report import generate_report
from core.report import get_data

from datetime import datetime


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
?? AURA AI Trader

œ” Ì«—  Õ·Ì· ÂÊ‘„‰œ »«“«— ›⁄«· ‘œ.

œ” Ê—« :

/report
ê“«—‘ ò«„· »«“«—

/top
›—’ ùÂ«Ì »— — AURA

/status
Ê÷⁄Ì  ”Ì” „

/id
‰„«Ì‘ Chat ID
"""

    await update.message.reply_text(text)



async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.message.chat.id

    await update.message.reply_text(
        f"Chat ID ‘„«:\n{chat_id}"
    )



async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        text = generate_report()

        await update.message.reply_text(
            text
        )

    except Exception as e:

        await update.message.reply_text(
            f"? Report Error:\n{e}"
        )



async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        data = get_data()


        if not data:

            await update.message.reply_text(
                "? ”Ìê‰«·Ì ÅÌœ« ‰‘œ"
            )

            return



        text = """
?? AURA TOP SIGNALS

"""


        for i, coin in enumerate(data[:5],1):

            text += f"""
{i}) {coin["‰«„"]} ({coin["‰„«œ"]})

?? Score:
{coin["«„ Ì«“ AURA"]}

?? Decision:
{coin[" ’„Ì„"]}

??????????

"""


        await update.message.reply_text(
            text
        )


    except Exception as e:

        await update.message.reply_text(
            f"? Error:\n{e}"
        )



async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        data = get_data()


        text = f"""
?? AURA STATUS

?? Bot:
Online

?? Market Engine:
OK

?? Technical Engine:
OK

?? Signals:
{len(data)}

?? Time:
{datetime.now().strftime("%Y-%m-%d %H:%M")}
"""

        await update.message.reply_text(
            text
        )


    except Exception as e:

        await update.message.reply_text(
            f"? Status Error:\n{e}"
        )



def run():

    app = Application.builder().token(
        TELEGRAM_TOKEN
    ).build()


    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("id", get_id)
    )

    app.add_handler(
        CommandHandler("report", report)
    )

    app.add_handler(
        CommandHandler("top", top)
    )

    app.add_handler(
        CommandHandler("status", status)
    )


    print(
        "AURA Bot Running"
    )


    app.run_polling()



if __name__ == "__main__":

    run()

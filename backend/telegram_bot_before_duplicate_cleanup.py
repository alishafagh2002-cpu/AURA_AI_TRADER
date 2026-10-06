# -*- coding: utf-8 -*-

from telegram import Update
from telegram.request import HTTPXRequest
from telegram.ext import Application, CommandHandler, ContextTypes

from config.settings import TELEGRAM_TOKEN
from core.report import generate_report, get_data
from core.alert_engine import alert_report
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




async def alerts(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        text = alert_report()

        await update.message.reply_text(
            text
        )

    except Exception as e:

        await update.message.reply_text(
            f"Alert Error:\n{e}"
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



async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        from core.history import get_history

        data = get_history()

        if not data:
            await update.message.reply_text(
                "📊 AURA History empty"
            )
            return


        text = "📊 AURA HISTORY\n\n"

        for item in data[-5:]:

            text += (
                f"{item['time']}\n"
                f"{str(item['data'])[:200]}\n"
                "----------------\n"
            )

        await update.message.reply_text(text)


    except Exception as e:

        await update.message.reply_text(
            f"History Error:\n{e}"
        )



async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        from core.alert_engine import alert_report

        await update.message.reply_text(
            alert_report()
        )


    except Exception as e:

        await update.message.reply_text(
            f"Scan Error:\n{e}"
        )





async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        from core.nobitex_live import balances as nobitex_balances

        data = nobitex_balances()

        if not data:
            await update.message.reply_text("NOBITEX BALANCE\n\nNo balance data")
            return

        lines = ["NOBITEX BALANCE", ""]

        for symbol, info in data.items():
            lines.append(
                f"{symbol}: balance={info.get('balance')} | "
                f"active={info.get('active')} | "
                f"blocked={info.get('blocked')}"
            )

        await update.message.reply_text("\n".join(lines))

    except Exception as e:
        await update.message.reply_text(f"Nobitex balance error:\n{e}")


async def positions(update: Update, context: ContextTypes.DEFAULT_TYPE):

    from core.portfolio import positions

    data = positions()

    if not data:
        await update.message.reply_text(
            "?? No open positions"
        )
        return

    text = "?? POSITIONS\n\n"

    for p in data:

        text += f"""
{p['symbol']}

Entry:
{p['entry']}

Quantity:
{p['qty']}

----------------
"""

    await update.message.reply_text(text)




async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):

    from core.paper_trader import buy as execute_buy


    if len(context.args) < 3:

        await update.message.reply_text(
            "Usage:\n/buy SYMBOL PRICE AMOUNT"
        )
        return


    result = execute_buy(
        context.args[0],
        float(context.args[1]),
        float(context.args[2])
    )


    await update.message.reply_text(result)


async def sell(update: Update, context: ContextTypes.DEFAULT_TYPE):

    from core.paper_trader import sell

    if not context.args:

        await update.message.reply_text(
            "Usage:\n/sell SYMBOL"
        )

        return


    result = sell(
        context.args[0]
    )


    await update.message.reply_text(
        result
    )





async def pnl(update: Update, context: ContextTypes.DEFAULT_TYPE):

    from core.pnl_engine import calculate_pnl


    from core.live_price import get_live_price

    prices = {
        "MON": get_live_price("MON")
    }


    data = calculate_pnl(prices)


    if not data:

        await update.message.reply_text(
            "No positions"
        )

        return


    text = "?? AURA PNL\n\n"


    for p in data:

        text += f"""
{p['symbol']}

Entry:
{p['entry']}

Current:
{p['current']}

P/L:
{p['pnl']} USDT

Change:
{p['percent']}%

----------------
"""


    await update.message.reply_text(text)


async def monitor(update: Update, context: ContextTypes.DEFAULT_TYPE):

    from core.market import get_market
    from core.trader_manager import monitor


    market = get_market()


    prices = {}

    for c in market.values():

        prices[c["symbol"]] = c["price"]


    result = monitor(prices)


    if not result:

        await update.message.reply_text(
            "? No action"
        )

        return


    await update.message.reply_text(
        "\n".join(result)
    )




async def exchange_status(update: Update, context: ContextTypes.DEFAULT_TYPE):

    from core.exchange_live import account_status

    s = account_status()

    await update.message.reply_text(
        "EXCHANGE STATUS\n\n"
        f"Exchange: {s['exchange']}\n"
        f"Live trading: {s['live']}\n"
        f"API key: {s['api_key_set']}\n"
        f"Secret: {s['secret_set']}\n"
        f"Max trade: {s['max_trade_usdt']} USDT"
    )


async def real_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        from core.exchange_live import fetch_usdt_balance

        b = fetch_usdt_balance()

        await update.message.reply_text(
            "REAL USDT BALANCE\n\n"
            f"Free: {b['free']}\n"
            f"Used: {b['used']}\n"
            f"Total: {b['total']}"
        )

    except Exception as e:
        await update.message.reply_text(
            f"Balance error:\n{e}"
        )


async def real_buy(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) < 2:

        await update.message.reply_text(
            "Usage:\n/realbuy BTC 10"
        )
        return

    try:
        from core.exchange_live import market_buy_usdt

        result = market_buy_usdt(
            context.args[0],
            float(context.args[1])
        )

        await update.message.reply_text(
            f"{result}"
        )

    except Exception as e:
        await update.message.reply_text(
            f"Buy error:\n{e}"
        )


async def real_sell(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) < 2:

        await update.message.reply_text(
            "Usage:\n/realsell BTC 0.001"
        )
        return

    try:
        from core.exchange_live import market_sell

        result = market_sell(
            context.args[0],
            float(context.args[1])
        )

        await update.message.reply_text(
            f"{result}"
        )

    except Exception as e:
        await update.message.reply_text(
            f"Sell error:\n{e}"
        )




async def realbalance(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        from core.nobitex_live import balances

        data = balances()

        lines = ["NOBITEX REAL BALANCE", ""]

        for k, v in data.items():
            lines.append(
                f"{k}: balance={v.get('balance')} active={v.get('active')} blocked={v.get('blocked')}"
            )

        await update.message.reply_text("\n".join(lines))

    except Exception as e:
        await update.message.reply_text(f"realbalance error:\n{e}")


async def realbuy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text(
            "Usage:\n/realbuy BTC 100000\n\n"
            "Amount is in TOMAN."
        )
        return

    try:
        import requests
        from core.nobitex_live import place_limit_order

        symbol = context.args[0].lower()
        toman_amount = float(context.args[1])

        if toman_amount <= 0:
            await update.message.reply_text("Amount must be greater than zero.")
            return

        s = requests.Session()
        s.trust_env = False

        r = s.get(
            "https://api.nobitex.ir/market/stats",
            params={
                "srcCurrency": symbol,
                "dstCurrency": "rls"
            },
            timeout=30
        )

        r.raise_for_status()
        data = r.json()

        key = f"{symbol}-rls"

        if data.get("status") != "ok" or key not in data.get("stats", {}):
            await update.message.reply_text(
                f"Market data not available for {symbol.upper()}/RLS"
            )
            return

        stats = data["stats"][key]

        price_rls = float(stats.get("bestSell") or stats.get("latest"))

        if price_rls <= 0:
            await update.message.reply_text("Invalid market price.")
            return

        rls_amount = toman_amount * 10
        crypto_amount = rls_amount / price_rls

        result = place_limit_order(
            "buy",
            symbol,
            "rls",
            crypto_amount,
            price_rls
        )

        await update.message.reply_text(
            f"REAL BUY REQUEST\n\n"
            f"Asset: {symbol.upper()}\n"
            f"Budget: {toman_amount:,.0f} TOMAN\n"
            f"Price: {price_rls:,.0f} RLS\n"
            f"Amount: {crypto_amount:.10f}\n\n"
            f"Result:\n{result}"
        )

    except Exception as e:
        await update.message.reply_text(f"realbuy error:\n{e}")


async def realsell(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) < 4:
        await update.message.reply_text(
            "Usage:\n/realsell SYMBOL QUOTE AMOUNT PRICE\n\nExample:\n/realsell btc rls 0.0001 12000000000"
        )
        return

    try:
        from core.nobitex_live import place_limit_order

        result = place_limit_order(
            "sell",
            context.args[0],
            context.args[1],
            float(context.args[2]),
            float(context.args[3])
        )

        await update.message.reply_text(str(result))

    except Exception as e:
        await update.message.reply_text(f"realsell error:\n{e}")



def run():

    app = (
    Application.builder().token(
        TELEGRAM_TOKEN
    )
    .request(
        HTTPXRequest(
                    proxy="http://127.0.0.1:2080",
                    connect_timeout=30,
                    read_timeout=30,
                    write_timeout=30,
                    pool_timeout=30
                )
    )
    .get_updates_request(
        HTTPXRequest(
                    proxy="http://127.0.0.1:2080",
                    connect_timeout=30,
                    read_timeout=30,
                    write_timeout=30,
                    pool_timeout=30
                )
    )
    .build()
)


    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("id", get_id))
    app.add_handler(CommandHandler("report", report))
    app.add_handler(CommandHandler("top", top))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("alerts", alerts))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("positions", positions))
    app.add_handler(CommandHandler("buy", buy))
    app.add_handler(CommandHandler("sell", sell))
    app.add_handler(CommandHandler("pnl", pnl))
    app.add_handler(CommandHandler("exchange", exchange_status))
    app.add_handler(CommandHandler("realbalance", real_balance))
    app.add_handler(CommandHandler("realbuy", real_buy))
    app.add_handler(CommandHandler("realsell", real_sell))
    app.add_handler(CommandHandler("monitor", monitor))


    print("AURA Bot Running")


    app.run_polling()


if __name__ == "__main__":
    run()



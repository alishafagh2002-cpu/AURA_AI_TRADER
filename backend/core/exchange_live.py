
import os
import ccxt
from dotenv import load_dotenv

load_dotenv()

EXCHANGE_ID = os.getenv("EXCHANGE_ID", "bybit").lower()
API_KEY = os.getenv("EXCHANGE_API_KEY", "")
API_SECRET = os.getenv("EXCHANGE_API_SECRET", "")
PASSWORD = os.getenv("EXCHANGE_PASSWORD", "")
LIVE_TRADING = os.getenv("LIVE_TRADING", "false").lower() == "true"
MAX_TRADE_USDT = float(os.getenv("MAX_TRADE_USDT", "25"))


def get_exchange():

    if not hasattr(ccxt, EXCHANGE_ID):
        raise ValueError(f"Unsupported exchange: {EXCHANGE_ID}")

    cls = getattr(ccxt, EXCHANGE_ID)

    cfg = {
        "apiKey": API_KEY,
        "secret": API_SECRET,
        "enableRateLimit": True,
    }

    if PASSWORD:
        cfg["password"] = PASSWORD

    ex = cls(cfg)

    ex.load_markets()

    return ex


def account_status():

    return {
        "exchange": EXCHANGE_ID,
        "live": LIVE_TRADING,
        "api_key_set": bool(API_KEY),
        "secret_set": bool(API_SECRET),
        "max_trade_usdt": MAX_TRADE_USDT,
    }


def fetch_usdt_balance():

    ex = get_exchange()

    balance = ex.fetch_balance()

    usdt = balance.get("USDT", {})

    return {
        "free": usdt.get("free", 0),
        "used": usdt.get("used", 0),
        "total": usdt.get("total", 0),
    }


def market_buy_usdt(symbol, usdt_amount):

    if usdt_amount <= 0:
        raise ValueError("Amount must be > 0")

    if usdt_amount > MAX_TRADE_USDT:
        raise ValueError(
            f"Trade blocked: max allowed is {MAX_TRADE_USDT} USDT"
        )

    ex = get_exchange()

    market_symbol = f"{symbol.upper()}/USDT"

    if market_symbol not in ex.markets:
        raise ValueError(f"Market not found: {market_symbol}")

    ticker = ex.fetch_ticker(market_symbol)

    price = ticker.get("ask") or ticker.get("last")

    if not price:
        raise ValueError("Price unavailable")

    amount = usdt_amount / float(price)

    amount = float(ex.amount_to_precision(
        market_symbol,
        amount
    ))

    if not LIVE_TRADING:

        return {
            "mode": "DRY_RUN",
            "symbol": market_symbol,
            "side": "buy",
            "amount": amount,
            "price": price,
            "cost_estimate": usdt_amount,
        }

    return ex.create_order(
        market_symbol,
        "market",
        "buy",
        amount
    )


def market_sell(symbol, amount):

    if amount <= 0:
        raise ValueError("Amount must be > 0")

    ex = get_exchange()

    market_symbol = f"{symbol.upper()}/USDT"

    if market_symbol not in ex.markets:
        raise ValueError(f"Market not found: {market_symbol}")

    amount = float(ex.amount_to_precision(
        market_symbol,
        amount
    ))

    if not LIVE_TRADING:

        ticker = ex.fetch_ticker(market_symbol)

        return {
            "mode": "DRY_RUN",
            "symbol": market_symbol,
            "side": "sell",
            "amount": amount,
            "price": ticker.get("bid") or ticker.get("last"),
        }

    return ex.create_order(
        market_symbol,
        "market",
        "sell",
        amount
    )

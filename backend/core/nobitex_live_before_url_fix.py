
import os
import uuid
import requests
from dotenv import load_dotenv

load_dotenv()

session = requests.Session()
session.trust_env = False

BASE = "https://" + "apiv2" + "." + "nobitex" + "." + "ir"
ORDER_BASE = "https://" + "apiv2" + "." + "nobitex" + "." + "ir"

TOKEN = os.getenv("NOBITEX_TOKEN", "").strip()
LIVE = os.getenv("LIVE_TRADING", "false").lower() == "true"
MAX_TRADE_TOMAN = float(os.getenv("MAX_TRADE_TOMAN", "500000"))


def _headers():
    if not TOKEN:
        raise RuntimeError("NOBITEX_TOKEN is missing in .env")

    return {
        "Authorization": f"Token {TOKEN}",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "TraderBot/AURA-1.0"
    }


def status():
    return {
        "exchange": "nobitex",
        "token_set": bool(TOKEN),
        "live": LIVE,
        "max_trade_toman": MAX_TRADE_TOMAN
    }


def wallets():
    r = session.get(
        BASE + "/users/wallets/list",
        headers=_headers(),
        timeout=30
    )
    r.raise_for_status()
    return r.json()


def balances():
    data = wallets()

    result = {}

    for w in data.get("wallets", []):
        result[w.get("currency", "").upper()] = {
            "balance": w.get("balance"),
            "active": w.get("activeBalance"),
            "blocked": w.get("blockedBalance")
        }

    return result


def place_limit_order(side, symbol, quote, amount, price):

    side = side.lower().strip()
    symbol = symbol.lower().strip()
    quote = quote.lower().strip()

    if side not in ("buy", "sell"):
        raise ValueError("side must be buy or sell")

    if quote not in ("rls", "usdt"):
        raise ValueError("quote must be rls or usdt")

    amount = float(amount)
    price = float(price)

    if amount <= 0 or price <= 0:
        raise ValueError("amount and price must be positive")

    if quote == "rls":
        toman_value = (amount * price) / 10

        if toman_value > MAX_TRADE_TOMAN:
            raise ValueError(
                f"Trade blocked: max allowed is {MAX_TRADE_TOMAN} toman"
            )

    payload = {
        "type": side,
        "srcCurrency": symbol,
        "dstCurrency": quote,
        "amount": str(amount),
        "price": str(price),
        "clientOrderId": "aura-" + uuid.uuid4().hex[:20]
    }

    if not LIVE:
        return {
            "mode": "DRY_RUN",
            "endpoint": "/market/orders/add",
            "payload": payload
        }

    r = session.post(
        ORDER_BASE + "/market/orders/add",
        headers=_headers(),
        json=payload,
        timeout=30
    )

    r.raise_for_status()

    return r.json()

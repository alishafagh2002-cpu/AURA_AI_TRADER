import os
import json
import time
import base64
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

load_dotenv()

BASE = "https://apiv2.nobitex.ir"

API_KEY = os.getenv("NOBITEX_API_KEY", "").strip()
PRIVATE_KEY_B64 = os.getenv("NOBITEX_PRIVATE_KEY", "").strip()

LIVE = os.getenv("LIVE_TRADING", "false").lower() == "true"
MAX_TRADE_TOMAN = float(os.getenv("MAX_TRADE_TOMAN", "50000"))

session = requests.Session()
session.trust_env = False


def _b64decode(value: str) -> bytes:
    value = value.strip()
    value += "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value.encode())


def _private_key():
    if not PRIVATE_KEY_B64:
        raise RuntimeError("NOBITEX_PRIVATE_KEY is missing")

    raw = _b64decode(PRIVATE_KEY_B64)

    if len(raw) != 32:
        raise RuntimeError(
            f"Invalid Nobitex private key length: {len(raw)} bytes"
        )

    return Ed25519PrivateKey.from_private_bytes(raw)


def _headers(method: str, full_path: str, raw_body: str = ""):
    if not API_KEY:
        raise RuntimeError("NOBITEX_API_KEY is missing")

    timestamp = str(int(time.time()))

    message = (
        timestamp
        + method.upper()
        + full_path
        + raw_body
    ).encode("utf-8")

    signature = _private_key().sign(message)

    signature_b64 = base64.urlsafe_b64encode(
        signature
    ).decode("ascii")

    return {
        "Content-Type": "application/json",
        "Nobitex-Key": API_KEY,
        "Nobitex-Signature": signature_b64,
        "Nobitex-Timestamp": timestamp,
    }


def request(method, path, params=None, payload=None, timeout=20):
    method = method.upper()

    full_path = path

    if params:
        qs = urlencode(params)
        full_path += "?" + qs

    raw_body = ""

    if payload is not None:
        raw_body = json.dumps(
            payload,
            separators=(",", ":"),
            ensure_ascii=False,
        )

    headers = _headers(
        method=method,
        full_path=full_path,
        raw_body=raw_body,
    )

    url = BASE + full_path

    response = session.request(
        method=method,
        url=url,
        headers=headers,
        data=raw_body if payload is not None else None,
        timeout=timeout,
    )

    try:
        data = response.json()
    except Exception:
        data = {
            "status_code": response.status_code,
            "text": response.text,
        }

    if not response.ok:
        raise RuntimeError(
            f"Nobitex API error {response.status_code}: {data}"
        )

    return data


def status():
    return {
        "exchange": "nobitex",
        "api_key_set": bool(API_KEY),
        "private_key_set": bool(PRIVATE_KEY_B64),
        "token_set": bool(API_KEY),
        "live": LIVE,
        "max_trade_toman": MAX_TRADE_TOMAN,
    }


def balances():
    return request(
        "GET",
        "/users/wallets/list",
    )


def place_limit_order(
    side,
    symbol,
    quote,
    amount,
    price,
):
    side = str(side).lower().strip()
    symbol = str(symbol).lower().strip()
    quote = str(quote).lower().strip()

    amount = float(amount)
    price = float(price)

    if side not in ("buy", "sell"):
        raise ValueError("side must be buy or sell")

    if quote not in ("rls", "usdt"):
        raise ValueError("quote must be rls or usdt")

    if amount <= 0 or price <= 0:
        raise ValueError("amount and price must be positive")

    order_value = amount * price

    if quote == "rls":
        order_value_toman = order_value / 10

        if order_value_toman > MAX_TRADE_TOMAN:
            raise ValueError(
                f"Trade blocked: {order_value_toman:,.0f} TOMAN "
                f"> MAX_TRADE_TOMAN={MAX_TRADE_TOMAN:,.0f}"
            )

    payload = {
        "type": side,
        "srcCurrency": symbol,
        "dstCurrency": quote,
        "amount": format(amount, ".12f").rstrip("0").rstrip("."),
        "price": format(price, ".8f").rstrip("0").rstrip("."),
    }

    if not LIVE:
        return {
            "mode": "DRY_RUN",
            "endpoint": "/market/orders/add",
            "payload": payload,
        }

    return request(
        "POST",
        "/market/orders/add",
        payload=payload,
    )

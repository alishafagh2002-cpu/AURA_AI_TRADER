
from core.portfolio import load


def calculate_pnl(prices):

    data = load()

    result = []

    for p in data["positions"]:

        symbol = p["symbol"]

        if symbol not in prices:
            continue

        current = prices[symbol]

        pnl = (current - p["entry"]) * p["qty"]

        percent = (
            (current - p["entry"])
            / p["entry"]
        ) * 100


        result.append({
            "symbol": symbol,
            "entry": p["entry"],
            "current": current,
            "pnl": round(pnl,2),
            "percent": round(percent,2)
        })


    return result

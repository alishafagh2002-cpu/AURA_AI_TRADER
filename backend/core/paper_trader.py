
from core.portfolio import load, save
from datetime import datetime


def buy(symbol, price, amount):

    data = load()

    if data["balance"] < amount:
        return "Not enough balance"

    qty = amount / price

    data["balance"] -= amount

    data["positions"].append({
        "symbol": symbol,
        "entry": price,
        "qty": qty,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M")
    })

    save(data)

    return "BUY executed"


def sell(symbol):

    data = load()

    for p in data["positions"]:
        if p["symbol"] == symbol:

            data["balance"] += p["qty"] * p["entry"]

            data["positions"].remove(p)

            save(data)

            return "SELL executed"

    return "Position not found"


from core.portfolio import load, save


STOP = -3
TARGET = 8


def monitor(prices):

    data = load()

    actions=[]


    for p in data["positions"][:]:

        symbol=p["symbol"]

        if symbol not in prices:
            continue


        current=prices[symbol]

        change=((current-p["entry"])/p["entry"])*100


        value=current*p["qty"]


        if change <= STOP:

            data["balance"] += value

            data["positions"].remove(p)

            actions.append(
                f"?? STOP LOSS {symbol}\n{change:.2f}%"
            )


        elif change >= TARGET:

            data["balance"] += value

            data["positions"].remove(p)

            actions.append(
                f"?? TAKE PROFIT {symbol}\n{change:.2f}%"
            )


    save(data)

    return actions


from core.market import get_market


def get_live_price(symbol):

    try:

        data = get_market()

        for coin in data.values():

            if coin.get("symbol") == symbol:

                return coin.get("price")


        return None


    except Exception as e:

        print(e)

        return None

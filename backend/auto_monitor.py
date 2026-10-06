
import time

from core.market import get_market
from core.trader_manager import monitor


while True:

    try:

        market = get_market()

        prices = {}

        for c in market.values():

            prices[c["symbol"]] = c["price"]


        result = monitor(prices)


        if result:

            print(result)


    except Exception as e:

        print(e)


    time.sleep(60)

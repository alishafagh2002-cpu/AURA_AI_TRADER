import requests
import time


def get_candles(symbol="bitcoin", days=7):

    url = f"https://api.coingecko.com/api/v3/coins/{symbol}/market_chart"


    params = {

        "vs_currency": "usd",

        "days": days,

        "interval": "hourly"

    }


    try:

        response = requests.get(
            url,
            params=params,
            timeout=20,
            headers={
                "User-Agent":"AURA-AI-Trader"
            }
        )


        data = response.json()


        if "prices" not in data:

            return []


        candles = []


        for p in data["prices"]:

            candles.append({

                "close": p[1]

            })


        return candles


    except Exception:

        return []

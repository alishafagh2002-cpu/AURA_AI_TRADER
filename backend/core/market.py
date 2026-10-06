import requests
import json
import os
import time


CACHE_FILE = "market_cache.json"


def load_cache():

    if not os.path.exists(CACHE_FILE):
        return None

    try:

        with open(
            CACHE_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            cache = json.load(f)


        return cache["data"]

    except:

        return None



def save_cache(data):

    with open(
        CACHE_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            {
                "time": time.time(),
                "data": data
            },
            f,
            ensure_ascii=False
        )



def get_market():

    cached = load_cache()


    url = "https://api.coingecko.com/api/v3/coins/markets"


    params = {

        "vs_currency":"usd",

        "order":"volume_desc",

        "per_page":50,

        "page":1,

        "sparkline":"false"

    }


    for attempt in range(3):

        try:

            response = requests.get(
                url,
                params=params,
                timeout=30,
                headers={
                    "User-Agent":
                    "Mozilla/5.0 AURA-AI"
                }
            )


            if response.status_code == 200:

                coins = response.json()

                result = {}


                for coin in coins:

                    result[coin["id"]] = {

                        "name":coin["name"],

                        "symbol":
                        coin["symbol"].upper(),

                        "price":
                        coin["current_price"],

                        "change":
                        coin.get(
                            "price_change_percentage_24h",
                            0
                        ),

                        "volume":
                        coin["total_volume"],

                        "market_cap":
                        coin["market_cap"]

                    }


                save_cache(result)

                return result


        except Exception as e:

            print(
                "Market retry:",
                attempt+1,
                e
            )


        time.sleep(3)



    if cached:

        print(
            "Using cache"
        )

        return cached



    raise Exception(
        "Market unavailable"
    )

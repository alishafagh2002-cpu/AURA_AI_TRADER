import json
import os
import time


CACHE_FILE = "market_cache.json"


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


def load_cache():

    if not os.path.exists(CACHE_FILE):
        return None


    with open(
        CACHE_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        cache = json.load(f)


    # اعتبار 5 دقیقه
    if time.time() - cache["time"] < 300:

        return cache["data"]


    return None

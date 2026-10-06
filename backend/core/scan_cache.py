import json
import os
import time


CACHE_FILE = "aura_scan_cache.json"


def save_scan(data):

    payload = {

        "time": time.time(),

        "data": data

    }


    with open(
        CACHE_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            payload,
            f,
            ensure_ascii=False,
            indent=2
        )



def load_scan(max_age=1800):

    if not os.path.exists(CACHE_FILE):

        return None


    try:

        with open(
            CACHE_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            payload = json.load(f)



        age = time.time() - payload["time"]


        if age > max_age:

            return None


        return payload["data"]


    except:

        return None

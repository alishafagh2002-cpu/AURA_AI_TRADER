import json
import os
from datetime import datetime


FILE="signal_history.json"


def save_signal(data):

    history=[]

    if os.path.exists(FILE):
        with open(FILE,"r",encoding="utf-8") as f:
            history=json.load(f)


    history.append({
        "time":datetime.now().strftime("%Y-%m-%d %H:%M"),
        "data":data
    })


    with open(FILE,"w",encoding="utf-8") as f:
        json.dump(
            history,
            f,
            ensure_ascii=False,
            indent=2
        )


def get_history():

    if not os.path.exists(FILE):
        return []

    with open(FILE,"r",encoding="utf-8") as f:
        return json.load(f)

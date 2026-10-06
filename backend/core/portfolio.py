
import json
import os

FILE = "portfolio.json"

def load():

    if not os.path.exists(FILE):
        return {
            "balance": 1000,
            "positions": []
        }

    with open(FILE,"r",encoding="utf-8") as f:
        return json.load(f)


def save(data):

    with open(FILE,"w",encoding="utf-8") as f:
        json.dump(data,f,ensure_ascii=False,indent=2)


def balance():
    return load()["balance"]


def positions():
    return load()["positions"]

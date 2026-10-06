from core.market import get_market
from core.candles import get_candles
from core.technical import technical_analysis


def aura_scan():

    market = get_market()

    results = []


    candidates = []


    for coin_id, info in market.items():

        candidates.append({

            "id": coin_id,
            "name": info["name"],
            "symbol": info["symbol"],
            "price": info["price"],
            "change": info["change"] or 0,
            "volume": info["volume"]

        })


    candidates.sort(
        key=lambda x:x["change"],
        reverse=True
    )


    candidates = candidates[:20]


    for coin in candidates:

        try:

            candles = get_candles(
                coin["id"]
            )


            if len(candles) < 20:
                continue


            tech = technical_analysis(
                candles
            )


            if tech["MACD"] == "نامشخص":
                continue


            if tech["EMA"] == "نامشخص":
                continue


            tech_score = int(
                tech["امتیاز تکنیکال"].split("/")[0]
            )


            momentum = min(
                max(coin["change"],0),
                20
            )


            score = int(
                tech_score * 0.7
                +
                momentum
            )


            score = max(
                0,
                min(score,100)
            )


            if score >= 75:
                decision="🟢 فرصت بررسی خرید"

            elif score >=55:
                decision="🟡 زیر نظر"

            else:
                decision="🔴 عدم ورود"


            results.append({

                "نام":coin["name"],

                "نماد":coin["symbol"],

                "قیمت":coin["price"],

                "تغییر ۲۴ ساعت":coin["change"],

                "RSI":tech["RSI"],

                "MACD":tech["MACD"],

                "EMA":tech["EMA"],

                "امتیاز AURA":str(score)+"/100",

                "تصمیم":decision

            })


        except:

            continue


    results.sort(
        key=lambda x:int(
            x["امتیاز AURA"].split("/")[0]
        ),
        reverse=True
    )


    return results

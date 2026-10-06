import pandas as pd
import ta


def technical_analysis(prices):

    df = pd.DataFrame(prices)


    if "close" not in df.columns:

        return {
            "RSI": 0,
            "MACD": "نامشخص",
            "EMA": "نامشخص",
            "امتیاز تکنیکال": "0/100"
        }


    if len(df) < 30:

        return {
            "RSI": 0,
            "MACD": "نامشخص",
            "EMA": "نامشخص",
            "امتیاز تکنیکال": "0/100"
        }


    close = df["close"].astype(float)


    # RSI

    rsi = ta.momentum.RSIIndicator(
        close
    ).rsi().iloc[-1]


    # MACD

    macd = ta.trend.MACD(
        close
    )

    macd_value = macd.macd().iloc[-1]


    # EMA

    ema = ta.trend.EMAIndicator(
        close,
        window=20
    ).ema_indicator().iloc[-1]


    current = close.iloc[-1]


    score = 50


    if rsi < 30:
        score += 15

    elif rsi > 70:
        score -= 10


    if macd_value > 0:
        score += 10

    else:
        score -= 5


    if current > ema:
        score += 10

    else:
        score -= 5


    score = max(0, min(score, 100))


    return {

        "RSI": round(float(rsi), 2),

        "MACD":
        "مثبت" if macd_value > 0 else "منفی",

        "EMA":
        "بالای روند" if current > ema else "زیر روند",

        "امتیاز تکنیکال":
        str(score) + "/100"

    }
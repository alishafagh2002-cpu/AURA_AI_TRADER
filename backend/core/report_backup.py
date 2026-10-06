from core.aura_engine import aura_scan
from core.risk import calculate_risk
from datetime import datetime


def generate_report():

    data = aura_scan()


    if not data:

        return """
🤖 AURA v3 MARKET REPORT

⚠️ No valid signal found.
"""


    text = f"""
🤖 AURA v3 MARKET REPORT

🕒 Time:
{datetime.now().strftime("%Y-%m-%d %H:%M")}

📊 Valid Signals:
{len(data)}

"""


    for i, coin in enumerate(data[:3],1):

        score = int(
            coin["امتیاز AURA"].split("/")[0]
        )


        try:

            risk = calculate_risk(
                coin["قیمت"],
                score,
                coin["RSI"]
            )

        except Exception:

            risk = {

                "entry":"N/A",

                "stop_loss":"N/A",

                "target1":"N/A",

                "target2":"N/A",

                "risk":"Unknown",

                "confidence":
                str(score)+"%"

            }


        text += f"""

━━━━━━━━━━━━━━

🏆 Rank {i}

{coin["نام"]} ({coin["نماد"]})


💵 Price:
{coin["قیمت"]} USD


📈 Change:
{coin["تغییر ۲۴ ساعت"]}%


📊 Technical:

RSI: {coin["RSI"]}

MACD: {coin["MACD"]}

EMA: {coin["EMA"]}


🧠 AURA Score:

{coin["امتیاز AURA"]}


📍 Entry Zone:

{risk["entry"]}


🛑 Stop Loss:

{risk["stop_loss"]}


🎯 Target 1:

{risk["target1"]}


🎯 Target 2:

{risk["target2"]}


⚖️ Risk:

{risk["risk"]}


🎯 Confidence:

{risk["confidence"]}


📌 Decision:

{coin["تصمیم"]}

"""


    text += """

⚠️ Algorithmic analysis only.
"""


    return text

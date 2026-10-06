from core.aura_engine import aura_scan
from core.risk import calculate_risk
from core.scan_cache import save_scan, load_scan
from datetime import datetime



def get_data():

    data = load_scan()


    if data:

        return data


    data = aura_scan()


    save_scan(data)


    return data




def generate_report():

    data = get_data()


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


        risk = calculate_risk(
            coin["قیمت"],
            score,
            coin["RSI"]
        )


        text += f"""

━━━━━━━━━━━━━━

🏆 Rank {i}

{coin["نام"]} ({coin["نماد"]})


💵 Price:
{coin["قیمت"]} USD


📈 Change:
{coin["تغییر ۲۴ ساعت"]}%


🧠 AURA Score:

{coin["امتیاز AURA"]}


📍 Entry:

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

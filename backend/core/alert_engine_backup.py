from core.report import get_data


def get_alerts():

    data = get_data()


    alerts = []


    for coin in data:

        try:

            score = int(
                coin["امتیاز AURA"].split("/")[0]
            )


            if score >= 75:

                alerts.append(
                    {
                        "name": coin["نام"],
                        "symbol": coin["نماد"],
                        "price": coin["قیمت"],
                        "score": score,
                        "decision": coin["تصمیم"]
                    }
                )


        except Exception:

            continue


    return alerts



def alert_report():

    alerts = get_alerts()


    if not alerts:

        return None


    text = """
AURA ALERT

"""


    for coin in alerts:


        text += f"""
🚨 {coin["name"]} ({coin["symbol"]})

Price:
{coin["price"]}

Score:
{coin["score"]}/100

Decision:
{coin["decision"]}

----------------

"""


    return text

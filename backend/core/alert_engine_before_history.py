from core.report import get_data


def get_alerts():

    data = get_data()

    alerts = []


    for coin in data:

        try:

            score = int(
                coin["امتیاز AURA"].split("/")[0]
            )


            if score >= 65:

                level = "STRONG" if score >= 75 else "WATCH"


                alerts.append(
                    {
                        "name": coin["نام"],
                        "symbol": coin["نماد"],
                        "price": coin["قیمت"],
                        "score": score,
                        "level": level,
                        "decision": coin["تصمیم"]
                    }
                )


        except Exception:

            continue


    return alerts



def alert_report():

    alerts = get_alerts()


    if not alerts:

        return "AURA: No signals"



    text = """
AURA ALERTS

"""


    for coin in alerts:


        text += f"""
{coin["level"]}

{coin["name"]} ({coin["symbol"]})

Price:
{coin["price"]}

Score:
{coin["score"]}/100

Decision:
{coin["decision"]}

----------------

"""


    return text

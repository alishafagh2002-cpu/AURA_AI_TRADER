def calculate_risk(price, score, rsi):


    # تعیین ریسک بر اساس امتیاز

    if score >= 80:

        risk = "Low"

    elif score >= 60:

        risk = "Medium"

    else:

        risk = "High"



    # محدوده ورود

    entry_low = price * 0.98

    entry_high = price * 1.02



    # حد ضرر

    stop_loss = price * 0.95



    # اهداف

    target1 = price * 1.08

    target2 = price * 1.15



    # اصلاح بر اساس RSI

    if rsi >= 70:

        risk = "High"



    return {


        "entry":

        f"{round(entry_low,6)} - {round(entry_high,6)}",


        "stop_loss":

        round(stop_loss,6),


        "target1":

        round(target1,6),


        "target2":

        round(target2,6),


        "risk":

        risk,


        "confidence":

        str(score)+"%"


    }

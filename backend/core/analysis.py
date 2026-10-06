def analyze(data):

    results = []


    for coin, info in data.items():


        score = 50


        change = info.get("change") or 0

        volume = info.get("volume") or 0


        # حرکت مثبت بازار

        if change > 0:
            score += 10


        if change > 3:
            score += 15


        if change < -3:
            score -= 15



        # حجم بالا

        if volume > 100000000:
            score += 10


        elif volume < 10000000:
            score -= 5



        # محدود کردن امتیاز

        if score > 100:
            score = 100


        if score < 0:
            score = 0



        if score >= 80:

            decision = "🟢 فرصت بررسی خرید"


        elif score >= 65:

            decision = "🟡 زیر نظر گرفتن"


        else:

            decision = "🔴 عدم ورود"



        results.append({

            "نام": info["name"],

            "نماد": info["symbol"],

            "قیمت": info["price"],

            "تغییر ۲۴ ساعت": round(change,2),

            "حجم": info["volume"],

            "امتیاز AURA": str(score)+"/100",

            "تصمیم": decision

        })



    results.sort(

        key=lambda x:int(
            x["امتیاز AURA"].split("/")[0]
        ),

        reverse=True

    )



    return {

        "🤖 ربات": "AURA",

        "🏆 بهترین فرصت": results[:5],

        "📊 تعداد بررسی شده": len(results)

    }

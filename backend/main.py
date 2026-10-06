from fastapi import FastAPI
from core.market import get_market
from core.analysis import analyze

app = FastAPI(
    title="AURA AI Trader"
)

@app.get("/")
def home():
    return {
        "status":"AURA فعال است",
        "message":"ربات آماده تحلیل بازار است"
    }

@app.get("/analyze")
def market_analysis():
    data = get_market()
    return analyze(data)

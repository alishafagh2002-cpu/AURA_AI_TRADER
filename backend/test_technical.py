from core.candles import get_candles
from core.technical import technical_analysis


candles = get_candles("bitcoin")


result = technical_analysis(candles)


print(result)

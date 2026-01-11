import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD
from data import crypto
from sentiment import sentiment_score

def analyze(symbol="BTCUSDT", risk="low"):
    prices = crypto(symbol)
    s = pd.Series(prices)

    rsi = RSIIndicator(s).rsi().iloc[-1]
    macd = MACD(s).macd().iloc[-1]
    ma50 = s.rolling(50).mean().iloc[-1]
    price = prices[-1]

    sentiment = sentiment_score()

    # Simple scoring system
    score = 0
    if rsi < 30: score += 2
    if macd > 0: score += 2
    if price > ma50: score += 2
    if sentiment > 0.5: score += 1

    if score >= 6:
        signal = "FAVORABLE"
    elif score >= 4:
        signal = "OBSERVE"
    else:
        signal = "WAIT"

    return {
        "price": price,
        "rsi": round(rsi, 2),
        "macd": round(macd, 2),
        "score": score,
        "signal": signal
    }

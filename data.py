import requests

def crypto(symbol="BTCUSDT"):
    """Fetch last 100 hourly closing prices from Binance"""
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1h&limit=100"
    data = requests.get(url).json()
    closes = [float(i[4]) for i in data]
    return closes

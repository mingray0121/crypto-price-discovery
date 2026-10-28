import requests
import pandas as pd

BINANCE_URL = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=5"
OKX_URL = "https://www.okx.com/api/v5/market/history-candles?instId=BTC-USDT&bar=1H&limit=5"
BYBIT_URL = "https://api.bybit.com/v5/market/kline?category=spot&symbol=BTCUSDT&interval=60&limit=5"
KRAKEN_URL = "https://api.kraken.com/0/public/OHLC?pair=XBTUSDT&interval=60"

api_dict = {
    "Binance": BINANCE_URL,
    "OKX": OKX_URL,
    "Bybit": BYBIT_URL,
    "Kraken": KRAKEN_URL}

def parse_binance(data):
    df = pd.DataFrame(data)
    df["time"] = pd.to_datetime(df[0].astype("int64"), unit="ms", utc=True)
    df["binance"] = df[4].astype(float)        
    return df.set_index("time")[["binance"]]
def parse_okx(data):
    df = pd.DataFrame(data["data"])
    df["time"] = pd.to_datetime(df[0].astype("int64"), unit="ms", utc=True)
    df["okx"] = df[4].astype(float)        
    return df.set_index("time")[["okx"]]
def parse_bybit(data):
    df = pd.DataFrame(data["result"]["list"])
    df["time"] = pd.to_datetime(df[0].astype("int64"), unit="ms", utc=True)
    df["bybit"] = df[4].astype(float)        
    return df.set_index("time")[["bybit"]]
def parse_kraken(data):
    df = pd.DataFrame(data["result"]["XBTUSDT"])
    df["time"] = pd.to_datetime(df[0].astype("int64"), unit="s", utc=True)
    df["kraken"] = df[4].astype(float)        
    return df.set_index("time")[["kraken"]]


for name, url in api_dict.items():
    try:
        r = requests.get(url = url, timeout=10)
        print(name, r.status_code)
        if name == "Binance":
            b = parse_binance(r.json())
        if name == "OKX":
            o = parse_okx(r.json())
        if name == "Bybit":
            y = parse_bybit(r.json())
        if name == "Kraken":
            k = parse_kraken(r.json())
    except requests.exceptions.RequestException as e:
        print(name, e)

merged = pd.concat([b, o, y, k], axis=1, join="inner").sort_index()
print(merged)

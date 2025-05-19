import pandas as pd
import talib as ta
import config 
from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.orders as orders
from datetime import datetime, timezone
import time

# Creates a connection to the OANDA API
client = API(access_token=config.OANDA_API_KEY)

# Define variables
instrument = "GBP_JPY"
timeframe = "M15"

def get_candles(tf):
    params = {
        "granularity": tf,
        "price": "A" # Ask prices
    }

    # Gets the candle data
    r = instruments.InstrumentsCandles(instrument=instrument, params=params)
    candles = client.request(r)['candles']

    # Converts the data to a pandas DataFrame
    data = []
    for candle in candles:
        if candle["complete"]: # Only include complete candles
            data.append({
                "time": candle["time"],
                "open": float(candle["ask"]["o"]),
                "high": float(candle["ask"]["h"]),
                "low": float(candle["ask"]["l"]),
                "close": float(candle["ask"]["c"])
            })

    df = pd.DataFrame(data)
    df["time"] = pd.to_datetime(df["time"])

    return df


# Function to calculate indicators

def calculate_indicators(df):
    # EMAs
    df["EMA_5"] = ta.EMA(df["close"], timeperiod=5)
    df["EMA_8"] = ta.EMA(df["close"], timeperiod=8)

    # ATR
    df["ATR_14"] = ta.ATR(df["high"], df["low"], df["close"], timeperiod=14)

    return df


# Function to check for EMA crossover signals
def ema_crossover(df):
    tp_ratio = 1.5 # 1.5 : 1 TP/SL ratio

    # Checks if the 5-period EMA crosses above the 8-period EMA
    last_candle = df.iloc[-1]
    prev_candle = df.iloc[-2]
    
    # Crossover Buy Signal (EMA 5 crosses above EMA 8)
    if last_candle["EMA_5"] > last_candle["EMA_8"] and prev_candle["EMA_5"] <= prev_candle["EMA_8"]:
        print("Buy Signal: EMA 5 crossed above EMA 8")
        entry_price = last_candle["close"]
        stop_loss = entry_price - df["ATR_14"]
        stop_distance = entry_price - stop_loss
        take_profit = entry_price + (stop_distance * tp_ratio)
        place_order(stop_loss, take_profit)
    else:
        print("Strategy conditions not met")


# Function to place an order

def place_order(sl, tp):
    data = {
        "order": {
            "instrument": instrument,
            "units": 1, # Number of units to trade
            "type": "MARKET",
            "stopLossOnFill": {"price": f"{sl:.3f}"}, # price is formatted to 3 decimal places
            "takeProfitOnFill": {"price": f"{tp:.3f}"}, 
        }
    }

    r = orders.OrderCreate(config.OANDA_ACCOUNT_ID, data=data)
    client.request(r)
    print(f"Placed order for {instrument} with SL: {sl:.3f} and TP: {tp:.3f}")



def run_bot():
    print ("Starting bot...")
    last_checked = None

    while True:
        current_time = datetime.now(timezone.utc)

        # Check for a new 15 minute candle
        if current_time.minute % 15 == 0 and current_time.second < 10:
            # Check if the 15-minute candle has changed since the last check
            if last_checked != current_time.minute:
                print("Checking for trade signals...")
                price = get_candles(timeframe)
                price = calculate_indicators(price)
                ema_crossover(price)
                last_checked = current_time.minute # Update to prevent multiple checks of the same candle

        time.sleep(1)


run_bot()

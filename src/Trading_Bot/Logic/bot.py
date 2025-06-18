import pandas as pd
import talib as ta
from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.orders as orders
from datetime import datetime, timezone
import time
import Trading_Bot.config as config


class Bot():
    def __init__(main_frame):
        client = API(access_token=config.OANDA_API_KEY)
        
    def get_candles(self, tf, instrument, log):
        params = {
            "granularity": tf,
            "price": "A", # Ask prices
            "count": 200 # Request more candles to ensure enough data for indicators
        }

        r = instrument.InstrumentsCandles(instrument=instrument, params=params)
        try:
            candles = client.request(r)['candles']
        except Exception as e:
            log.add_log.ERROR(f"Error fetching candles: {e}")
            return pd.DataFrame() # Return empty DataFrame on error

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


# Creates a connection to the OANDA API
client = API(access_token=config.OANDA_API_KEY)

def get_candles(tf, instrument, log):
    """
    Fetches candle data from OANDA API for a given timeframe and instrument.
    Converts the data into a pandas DataFrame.
    """
    params = {
        "granularity": tf,
        "price": "A", # Ask prices
        "count": 200 # Request more candles to ensure enough data for indicators
    }

    # Gets the candle data
    r = instruments.InstrumentsCandles(instrument=instrument, params=params)
    try:
        candles = client.request(r)['candles']
    except Exception as e:
        log.add_log.ERROR(f"Error fetching candles: {e}")
        return pd.DataFrame() # Return empty DataFrame on error

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


def calculate_indicators(df):
    """
    Calculates EMA and ATR indicators for the DataFrame.
    Drops rows with NaN values after calculation to ensure clean data for signals.
    """
    if df.empty:
        print("DataFrame is empty, cannot calculate indicators.")
        return df

    # EMAs
    df["EMA_5"] = ta.EMA(df["close"], timeperiod=5)
    df["EMA_8"] = ta.EMA(df["close"], timeperiod=8)

    # ATR
    df["ATR_14"] = ta.ATR(df["high"], df["low"], df["close"], timeperiod=14)

    # IMPORTANT: Drop rows with NaN values after indicator calculation.
    # This ensures that all indicator values are present for signal checking.
    df.dropna(inplace=True)

    return df


def ema_crossover(df, log):
    """
    Checks for EMA crossover signals and places an order if a signal is detected.
    Ensures sufficient data is available before checking signals.
    """
    tp_ratio = 1.5 # 1.5 : 1 TP/SL ratio

    # Ensure there are enough complete rows after dropping NaNs for signal checking
    if len(df) < 2:
        print("Not enough data after indicator calculation to check for signals.")
        return

    # Get the last two complete candles
    last_candle = df.iloc[-1]
    prev_candle = df.iloc[-2]
    
    # Crossover Buy Signal (EMA 5 crosses above EMA 8)
    # Check if both last_candle and prev_candle have valid (non-NaN) EMA values
    if (pd.notna(last_candle["EMA_5"]) and pd.notna(last_candle["EMA_8"]) and
        pd.notna(prev_candle["EMA_5"]) and pd.notna(prev_candle["EMA_8"]) and
        last_candle["EMA_5"] > last_candle["EMA_8"] and 
        prev_candle["EMA_5"] <= prev_candle["EMA_8"]):
        
        log.add_log("Buy Signal: EMA 5 crossed above EMA 8")
        entry_price = last_candle["close"]
        
        # Corrected: Use last_candle["ATR_14"] for the current ATR value
        if pd.notna(last_candle["ATR_14"]):
            stop_loss = entry_price - last_candle["ATR_14"]
            stop_distance = entry_price - stop_loss
            take_profit = entry_price + (stop_distance * tp_ratio)
            place_order(stop_loss, take_profit, log)
        else:
            ("ATR_14 is NaN for the last candle, cannot place order.")
    else:
        log.add_log("Strategy conditions not met. No order placed.")


def place_order(sl, tp, instrument, log):
    # Places a market order with specified stop-loss and take-profit prices.
    data = {
        "order": {
            "instrument": instrument,
            "units": 1, # Number of units to trade (adjust as needed)
            "type": "MARKET",
            "stopLossOnFill": {"price": f"{sl:.3f}"}, # price is formatted to 3 decimal places
            "takeProfitOnFill": {"price": f"{tp:.3f}"}, 
        }
    }
    try:
        r = orders.OrderCreate(config.OANDA_ACCOUNT_ID, data=data)
        client.request(r)
        log.add_log(f"Placed order for {instrument} with SL: {sl:.3f} and TP: {tp:.3f}")
    except Exception as e:
        print(f"Error placing order: {e}")


def run_bot(running, timeframe, instrument, log):
    log.add_log('Starting bot...')
    last_checked_minute = -1 # Initialize with a value that won't match current_time.minute initially

    while running:
        current_time = datetime.now(timezone.utc)

        # Check for a new candle.
        # The condition `current_time.second < 10` helps ensure it triggers once at the start of the minute.
        if current_time.minute % 15 == 0 and current_time.second < 10:
            # Check if the 15-minute candle has changed since the last check
            if last_checked_minute != current_time.minute:
                log.add_log(f"Checking for trade signals at {current_time.strftime('%Y-%m-%d %H:%M:%S UTC')}...")
                
                price_df = get_candles(timeframe, instrument, log)
                if not price_df.empty:
                    price_df = calculate_indicators(price_df)
                    ema_crossover(price_df, log)
                else:
                    log.add_log("No candle data retrieved. Skipping signal check.")
                
                last_checked_minute = current_time.minute # Update to prevent multiple checks of the same candle
        
        # Sleep for a short duration to avoid excessive CPU usage
        time.sleep(1)
    
def stop_bot(self, log):
    log.add_log("Stopping bot...")
    self.running = False  
    self.stop_event.set()  # Signal the bot to stop

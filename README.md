A W.I.P trading bot which uses the OANDA API and a simple EMA crossover strategy (At the moment).

SETUP:
1. Create a file named "config.py" -> Define variables: "OANDA_API_KEY" & "OANDA_ACCOUNT_ID"
2. In bot.py, configure instrument of choice and the timeframe to check the EMAs on
3. In the run_bot function, change the if statement to check for the candle time period of your choice


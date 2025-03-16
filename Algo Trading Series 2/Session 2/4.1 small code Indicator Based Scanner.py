import pdb
import time
import datetime
import traceback
from Dhan_Tradehull import Tradehull
import pandas as pd
from pprint import pprint
import talib
import pandas_ta as ta


client_code = "1102790337"
token_id    = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzM1NTQ3ODE5LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMjc5MDMzNyJ9.xC4uOx0WmfKHjjNJbSWLsGWj3Aubuko47tnsBw-QlVQTcGkrBtnHwPPIDv0Hth3tbg96CyFtSHnGmy1ogB9eaQ"
tsl         = Tradehull(client_code,token_id)
watchlist   = ['ADANIPORTS', 'NATIONAL_SBIN', 'TATASTEEL', 'BALMLAWRIE' ,'BAJAJFINSV', 'RELIANCE', 'TCS', 'JSWSTEEL',  'HCLTECH', 'TECHM',  'NTPC', 'BHARTIARTL', 'WIPRO', 'BAJFINANCE', 'INDUSINDBK', 'KOTAKBANK', 'HINDALCO', 'ULTRACEMCO',   'AXISBANK', 'M&M', 'MARUTI', 'HEROMOTOCO',  'EICHERMOT', 'COALINDIA', 'TITAN', 'UPL', 'HINDUNILVR', 'ITC', 'NESTLEIND', 'APOLLOHOSP', 'ICICIBANK',  'GRASIM', 'BRITANNIA', 'ASIANPAINT',  'POWERGRID', 'SBILIFE', 'ONGC']


for name in watchlist:

	try:
		current_time          = datetime.datetime.now()
		print(f"Scanning        {name}")
		chart                 = tsl.get_historical_data(tradingsymbol = name,exchange = 'NSE',timeframe="5")
		chart                 = tsl.heikin_ashi(df=candlestick_chart)


		pdb.set_trace()
		chart['rsi']          = talib.RSI(chart['close'], timeperiod=14)
		chart['CDLENGULFING'] = talib.CDLENGULFING(chart['open'], chart['high'], chart['low'], chart['close'])

		indi = ta.supertrend(chart['high'], chart['low'], chart['close'], 7, 3)
		chart = pd.concat([chart, indi], axis=1, join='inner')


		
		cc   = chart.iloc[-2]
		cc_3 = chart.iloc[-3]


		# buy entry conditions
		bc1 = cc['rsi'] > 60
		bc2 = (cc['SUPERTd_7_3.0'] == 1) and (cc_3['SUPERTd_7_3.0'] == -1)


		# sell entry conditions
		sc1 = cc['rsi'] < 40
		sc2 = (cc['SUPERTd_7_3.0'] == -1) and (cc_3['SUPERTd_7_3.0'] == 1)


		if bc1 and bc2:
			print("buy ", name, "\t")


		if sc1 and sc2:
			print("sell ", name, "\t")

	except Exception as e:
		print(e)
		pass






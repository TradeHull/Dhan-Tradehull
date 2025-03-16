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


watchlist = ['ADANIPORTS', 'ADANIENT', 'SBIN', 'TATASTEEL', 'BAJAJFINSV', 'RELIANCE', 'TCS', 'JSWSTEEL',  'HCLTECH', 'TECHM',  'NTPC']

for name in watchlist:
	chart = tsl.get_historical_data(tradingsymbol = name,exchange = 'NSE',timeframe="5")


	# make inicators rsi
	chart['rsi'] = talib.RSI(chart['close'], timeperiod=14)

	# make inicators supertrend
	indi = ta.supertrend(chart['high'], chart['low'], chart['close'], 7, 3)
	chart = pd.concat([chart, indi], axis=1, join='inner')

	# make CDLENGULFING
	chart['CDLENGULFING'] = talib.CDLENGULFING(chart['open'], chart['high'], chart['low'], chart['close'])


	# completed_candle
	cc = chart.iloc[-2]


	# buy entry conditions
	bc1 = cc['rsi'] > 60
	bc2 = cc['SUPERTd_7_3.0'] == 1
	bc3 = cc['CDLENGULFING'] == 100	


	# sell entry conditions
	sc1 = cc['rsi'] < 40
	sc2 = cc['SUPERTd_7_3.0'] == -1
	sc3 = cc['CDLENGULFING'] == -100	


	if bc1 and bc2 and bc3:
		print("buy ", name)


	if sc1 and sc2 and sc3:
		print("sell ", name)















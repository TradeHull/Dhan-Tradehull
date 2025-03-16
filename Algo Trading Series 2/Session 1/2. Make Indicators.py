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


chart = tsl.get_historical_data(tradingsymbol = 'ACC',exchange = 'NSE',timeframe="5")
chart = chart.set_index(chart['timestamp'])
pdb.set_trace()




chart['hl2'] = (chart['high'] + chart['low'])/2
chart['sma'] = talib.SMA(chart['close'], timeperiod=14)
chart['mom'] = talib.MOM(chart['close'], timeperiod=21)


chart['macd'], chart['macdsignal'], chart['macdhist']       = talib.MACD(chart['close'], fastperiod=12, slowperiod=26, signalperiod=9)
chart['upperband'], chart['middleband'], chart['lowerband'] = talib.BBANDS(chart['close'], timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)



chart['rsi']        = talib.RSI(chart['close'], timeperiod=14)
chart['sma_on_rsi'] = talib.SMA(chart['rsi'], timeperiod=14) # sma on rsi ???


indi = ta.supertrend(chart['high'], chart['low'], chart['close'], 14, 3)
chart = pd.concat([chart, indi], axis=1, join='inner')



chart['CDLCLOSINGMARUBOZU'] = talib.CDLCLOSINGMARUBOZU(chart['open'], chart['high'], chart['low'], chart['close'])
chart['CDLDOJI']            = talib.CDLDOJI(chart['open'], chart['high'], chart['low'], chart['close'])


df[df["A"] > 0]

chart[chart["CDLDOJI"] == 100]
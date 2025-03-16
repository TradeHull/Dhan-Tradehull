import pdb
from Dhan_Tradehull_V2 import Tradehull
import pandas as pd
import talib
import time
import datetime

client_code = "client_code"
token_id = "token_id"


tsl = Tradehull(client_code,token_id)

available_balance = tsl.get_balance()
leveraged_margin  = available_balance*5
max_trades = 3
per_trade_margin = (leveraged_margin/max_trades)
max_loss = (available_balance*1)/100*-1

watchlist = ['ADANIPORTS', 'ADANIENT', 'SBIN', 'TATASTEEL', 'BAJAJFINSV', 'RELIANCE', 'TCS', 'JSWSTEEL',  'HCLTECH', 'TECHM',  'NTPC', 'BHARTIARTL', 'WIPRO', 'BAJFINANCE', 'INDUSINDBK', 'KOTAKBANK', 'HINDALCO', 'ULTRACEMCO',   'AXISBANK', 'M&M', 'MARUTI', 'HEROMOTOCO',  'EICHERMOT', 'COALINDIA', 'TITAN', 'UPL', 'HINDUNILVR', 'ITC', 'NESTLEIND', 'APOLLOHOSP', 'ICICIBANK',  'GRASIM', 'BRITANNIA', 'ASIANPAINT',  'POWERGRID', 'SBILIFE', 'ONGC']
traded_wathclist = []


while True:

	live_pnl = tsl.get_live_pnl()
	current_time = datetime.datetime.now().time()

	if current_time < datetime.time(9, 30):
		print("wait for market to start", current_time)
		continue

	if (current_time > datetime.time(15, 15)) or (live_pnl < max_loss):
		order_details = tsl.cancel_all_orders()
		print("Market is over, Bye Bye see you tomorrow", current_time)
		break


	for stock_name in watchlist:
		time.sleep(1)
		print(stock_name)

		chart_1          = tsl.get_historical_data(tradingsymbol = stock_name,exchange = 'NSE',timeframe="1")
		chart_5          = tsl.get_historical_data(tradingsymbol = stock_name,exchange = 'NSE',timeframe="5") # this call has been updated to get_historical_data call, 

		if (chart_1 is None) or (chart_5 is None) :
			continue

		if (chart_1.empty) or (chart_5.empty):
			continue


		# Conditions that are on 1 minute timeframe
		chart_1['rsi'] = talib.RSI(chart_1['close'], timeperiod=14) #pandas
		cc_1           = chart_1.iloc[-2]  #pandas  completed candle of 1 min timeframe
		uptrend        = cc_1['rsi'] > 50
		downtrend      = cc_1['rsi'] < 49


		# Conditions that are on 5 minute timeframe
		chart_5['upperband'], chart_5['middleband'], chart_5['lowerband'] = talib.BBANDS(chart_5['close'], timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
		cc_5           = chart_5.iloc[-1]   # pandas
		ub_breakout    = cc_5['high'] > cc_5['upperband']
		lb_breakout    = cc_5['low'] < cc_5['lowerband']

		no_repeat_order = stock_name not in traded_wathclist
		max_order_limit = len(traded_wathclist) <= max_trades


		if uptrend and ub_breakout and no_repeat_order and max_order_limit:
			print(stock_name, "is in uptrend, Buy this script")

			sl_price          = round((cc_1['close']*0.98),1)
			qty               = int(per_trade_margin/cc_1['close'])

			buy_entry_orderid = tsl.order_placement(stock_name,'NSE', 1, 0, 0, 'MARKET', 'BUY', 'MIS')
			sl_orderid        = tsl.order_placement(stock_name,'NSE', 1, 0, sl_price, 'STOPMARKET', 'SELL', 'MIS')
			traded_wathclist.append(stock_name)

		if downtrend and lb_breakout and no_repeat_order and max_order_limit:
			print(stock_name, "is in downtrend, Sell this script")

			sl_price          = round((cc_1['close']*1.02),1)
			qty               = int(per_trade_margin/cc_1['close'])

			buy_entry_orderid = tsl.order_placement(stock_name,'NSE', 1, 0, 0, 'MARKET', 'SELL', 'MIS')
			sl_orderid        = tsl.order_placement(stock_name,'NSE', 1, 0, sl_price, 'STOPMARKET', 'BUY', 'MIS')
			traded_wathclist.append(stock_name)



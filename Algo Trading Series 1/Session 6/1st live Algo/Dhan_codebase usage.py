import pdb
from Dhan_Tradehull import Tradehull
import pandas as pd
import talib

client_code = "1102790337"
token_id = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzI1NDMxNTc2LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMjc5MDMzNyJ9.sW4kUgmS2WS7RX24OqPF07vkAdiQko3ZAX3dsKeBu_SzHio_yUQjla4PPp9TbDEwzn8pw1MH1nh4MvHjb7MZ_g"
tsl = Tradehull(client_code,token_id)


available_balance = tsl.get_balance()
leveraged_margin  = available_balance*5
max_trades = 3
per_trade_margin = (leveraged_margin/max_trades)


watchlist = ['MOTHERSON', 'OFSS', 'MANAPPURAM', 'BSOFT', 'CHAMBLFERT', 'DIXON', 'NATIONALUM', 'DLF', 'IDEA', 'ADANIPORTS', 'SAIL', 'HINDCOPPER', 'INDIGO', 'RECLTD', 'PNB', 'HINDALCO', 'RBLBANK', 'GNFC', 'ALKEM', 'CONCOR', 'PFC', 'GODREJPROP', 'MARUTI', 'ADANIENT', 'ONGC', 'CANBK', 'OBEROIRLTY', 'BANDHANBNK', 'SBIN', 'HINDPETRO', 'CANFINHOME', 'TATAMOTORS', 'LALPATHLAB', 'MCX', 'TATACHEM', 'BHARTIARTL', 'INDIAMART', 'LUPIN', 'INDUSTOWER', 'VEDL', 'SHRIRAMFIN', 'POLYCAB', 'WIPRO', 'UBL', 'SRF', 'BHARATFORG', 'GRASIM', 'IEX', 'BATAINDIA', 'AARTIIND', 'TATASTEEL', 'UPL', 'HDFCBANK', 'LTF', 'TVSMOTOR', 'GMRINFRA', 'IOC', 'ABCAPITAL', 'ACC', 'IDFCFIRSTB', 'ABFRL', 'ZYDUSLIFE', 'GLENMARK', 'TATAPOWER', 'PEL', 'IDFC', 'LAURUSLABS', 'BANKBARODA', 'KOTAKBANK', 'CUB', 'GAIL', 'DABUR', 'TECHM', 'CHOLAFIN', 'BEL', 'SYNGENE', 'FEDERALBNK', 'NAVINFLUOR', 'AXISBANK', 'LT', 'ICICIGI', 'EXIDEIND', 'TATACOMM', 'RELIANCE', 'ICICIPRULI', 'IPCALAB', 'AUBANK', 'INDIACEM', 'GRANULES', 'HDFCAMC', 'COFORGE', 'LICHSGFIN', 'BAJAJFINSV', 'INFY', 'BRITANNIA', 'M&MFIN', 'BAJFINANCE', 'PIIND', 'DEEPAKNTR', 'SHREECEM', 'INDUSINDBK', 'DRREDDY', 'TCS', 'BPCL', 'PETRONET', 'NAUKRI', 'JSWSTEEL', 'MUTHOOTFIN', 'CUMMINSIND', 'CROMPTON', 'M&M', 'GODREJCP', 'IGL', 'BAJAJ-AUTO', 'HEROMOTOCO', 'AMBUJACEM', 'BIOCON', 'ULTRACEMCO', 'VOLTAS', 'BALRAMCHIN', 'SUNPHARMA', 'ASIANPAINT', 'COALINDIA', 'SUNTV', 'EICHERMOT', 'ESCORTS', 'HAL', 'ASTRAL', 'NMDC', 'ICICIBANK', 'TORNTPHARM', 'JUBLFOOD', 'METROPOLIS', 'RAMCOCEM', 'INDHOTEL', 'HINDUNILVR', 'TRENT', 'TITAN', 'JKCEMENT', 'ASHOKLEY', 'SBICARD', 'BERGEPAINT', 'JINDALSTEL', 'MFSL', 'BHEL', 'NESTLEIND', 'HDFCLIFE', 'COROMANDEL', 'DIVISLAB', 'ITC', 'TATACONSUM', 'APOLLOTYRE', 'AUROPHARMA', 'HCLTECH', 'LTTS', 'BALKRISIND', 'DALBHARAT', 'APOLLOHOSP', 'ABBOTINDIA', 'ATUL', 'UNITDSPR', 'PVRINOX', 'SIEMENS', 'SBILIFE', 'IRCTC', 'GUJGASLTD', 'BOSCHLTD', 'NTPC', 'POWERGRID', 'MARICO', 'HAVELLS', 'MPHASIS', 'COLPAL', 'CIPLA', 'MGL', 'ABB', 'PIDILITIND', 'MRF', 'LTIM', 'PAGEIND', 'PERSISTENT']

traded_wathclist = []



while True:
	for stock_name in watchlist:
		print(stock_name)

		chart = tsl.get_intraday_data(stock_name, 'NSE', 1)
		chart['rsi'] = talib.RSI(chart['close'], timeperiod=14) #pandas

		bc   = chart.iloc[-2] #pandas  breakout candle
		ic   = chart.iloc[-3] #pandas  inside candle
		ba_c = chart.iloc[-4] #pandas  base candle

		uptrend = bc['rsi'] > 50
		downtrend = bc['rsi'] < 49
		inside_candle_formed = (ba_c['high'] > ic['high']) and (ba_c['low'] < ic['low'])


		upper_side_breakout = bc['high'] > ba_c['high']
		down_side_breakout  = bc['low']  < ba_c['low']

		no_repeat_order = stock_name not in traded_wathclist
		max_order_limit = len(traded_wathclist) <= max_trades


		if uptrend and inside_candle_formed and upper_side_breakout and no_repeat_order and max_order_limit:
			print(stock_name, "is in uptrend, Buy this script")
			qty = int(per_trade_margin/bc['close'])
			buy_entry_orderid = tsl.order_placement(stock_name,'NSE', 1, 0, 0, 'MARKET', 'BUY', 'MIS')
			traded_wathclist.append(stock_name)



		if downtrend and inside_candle_formed and down_side_breakout and no_repeat_order and max_order_limit:
			print(stock_name, "is in downtrend SELL this script")
			qty = int(per_trade_margin/bc['close'])
			sell_entry_orderid = tsl.order_placement(stock_name,'NSE', 1, 0, 0, 'MARKET', 'SELL', 'MIS')
			traded_wathclist.append(stock_name)









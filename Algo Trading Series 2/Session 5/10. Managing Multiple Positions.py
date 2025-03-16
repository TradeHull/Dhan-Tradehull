import pdb
import time
import datetime
import traceback
from Dhan_Tradehull import Tradehull
import pandas as pd
from pprint import pprint
import talib
import pandas_ta as ta
import xlwings as xw


client_code = "1102790337"
token_id    = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzM1NTQ3ODE5LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMjc5MDMzNyJ9.xC4uOx0WmfKHjjNJbSWLsGWj3Aubuko47tnsBw-QlVQTcGkrBtnHwPPIDv0Hth3tbg96CyFtSHnGmy1ogB9eaQ"
tsl         = Tradehull(client_code,token_id)


watchlist     = ['ADANIPORTS', 'SBIN', 'TATASTEEL', 'BAJAJFINSV', 'RELIANCE', 'TCS']#, 'JSWSTEEL',  'HCLTECH', 'TECHM',  'NTPC', 'BHARTIARTL', 'WIPRO', 'BAJFINANCE', 'INDUSINDBK', 'KOTAKBANK', 'HINDALCO', 'ULTRACEMCO',   'AXISBANK', 'M&M', 'MARUTI', 'HEROMOTOCO',  'EICHERMOT', 'COALINDIA', 'TITAN', 'UPL', 'HINDUNILVR', 'ITC', 'NESTLEIND', 'APOLLOHOSP', 'ICICIBANK',  'GRASIM', 'BRITANNIA', 'ASIANPAINT',  'POWERGRID', 'SBILIFE', 'ONGC']
single_order  = {'name':None, 'date':None , 'entry_time': None, 'entry_price': None, 'buy_sell': None, 'qty': None, 'sl': None, 'exit_time': None, 'exit_price': None, 'pnl': None, 'remark': None, 'traded':None}
orderbook     = {}
wb            = xw.Book('Live Trade Data.xlsx')
sheet         = wb.sheets['Sheet1']
reentry       = "no" #"yes/no"

completed_orders_sheet = wb.sheets['completed_orders']
completed_orders       = []

for name in watchlist:
	orderbook[name] = single_order.copy()


while True:

	for name in watchlist:

		orderbook_df            = pd.DataFrame(orderbook).T
		sheet.range('A1').value = orderbook_df

		current_time          = datetime.datetime.now()
		print(f"Scanning        {name}")
		chart                 = tsl.get_historical_data(tradingsymbol = name,exchange = 'NSE',timeframe="5")

		chart['rsi']          = talib.RSI(chart['close'], timeperiod=14)


		cc  = chart.iloc[-2]

		# buy entry conditions
		bc1 = cc['rsi'] > 60
		bc2 = orderbook[name]['traded'] is None

		# sell entry conditions
		sc1 = cc['rsi'] < 40
		sc2 = orderbook[name]['traded'] is None

		if bc1 and bc2:
			print("buy ", name, "\t")
			orderbook[name]['name']           = name
			orderbook[name]['date']           = str(current_time.date())
			orderbook[name]['entry_time']     = str(current_time.time())[:8]
			orderbook[name]['buy_sell']       = "BUY"
			orderbook[name]['qty']            = 1


			entry_orderid                     = "entry_orderid"     # tsl.order_placement(tradingsymbol=name ,exchange='NSE', quantity=orderbook[name]['qty'], price=0, trigger_price=0,    order_type='MARKET',     transaction_type='BUY',   trade_type='MIS')
			orderbook[name]['entry_price']    = cc['close']         # tsl.get_executed_price(orderid=entry_orderid)


			orderbook[name]['tg']             = round(orderbook[name]['entry_price']*1.01, 1)
			orderbook[name]['sl']             = round(orderbook[name]['entry_price']*0.99, 1)
			sl_orderid                        = "sl_orderid"        # tsl.order_placement(tradingsymbol=name ,exchange='NSE', quantity=orderbook[name]['qty'], price=0, trigger_price=orderbook[name]['sl'], order_type='STOPMARKET', transaction_type ='SELL', trade_type='MIS')
			orderbook[name]['sl_orderid']     = sl_orderid         # tsl.get_executed_price(orderid=entry_orderid)

			orderbook[name]['traded']         = "yes"


		if orderbook[name]['traded'] == "yes":
			bought = orderbook[name]['buy_sell'] == "BUY"

			if bought:
				sl_hit    = tsl.get_order_status(orderid=orderbook[name]['sl_orderid']) == "Traded"
				tg_hit    = cc['close'] > orderbook[name]['tg']


				if sl_hit:
					orderbook[name]['exit_time']  = str(current_time.time())[:8]
					orderbook[name]['exit_price'] = tsl.get_executed_price(orderid=orderbook[name]['sl_orderid'])
					orderbook[name]['pnl']        = (orderbook[name]['exit_price'] - orderbook[name]['entry_price'])*orderbook[name]['qty']
					orderbook[name]['remark']     = "Bought_SL_hit"

					if reentry == "yes":
						completed_orders.append(orderbook[name])
						orderbook[name] = None



				if tg_hit:
					tsl.cancel_order(OrderID=orderbook[name]['sl_orderid'])
					square_off_buy_order          = tsl.order_placement(tradingsymbol=orderbook[name]['name'] ,exchange='NSE', quantity=orderbook[name]['qty'], price=0, trigger_price=0,    order_type='MARKET',     transaction_type='SELL',   trade_type='MIS')
					orderbook[name]['exit_time']  = str(current_time.time())[:8]
					orderbook[name]['exit_price'] = tsl.get_executed_price(orderid=square_off_buy_order)
					orderbook[name]['pnl']        = (orderbook[name]['exit_price'] - orderbook[name]['entry_price'])*orderbook[name]['qty']
					orderbook[name]['remark']     = "Bought_TG_hit"

					if reentry == "yes":
						completed_orders.append(orderbook[name])
						orderbook[name] = None




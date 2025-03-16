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
import winsound
import sqn_lib


client_code = "1102790337"
token_id    = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzM2ODYwMTMxLCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMjc5MDMzNyJ9.Leop6waGeVfmBOtczNEcjRWmC8pUGWQf54YPINGDi_PZjk1IvW-DDdaYXsgM_s8McOT44q4MjEQxGXU0lduK0A"
tsl         = Tradehull(client_code,token_id)


opening_balance      = 1005000 # tsl.get_balance()
base_capital         = 1000000
market_money         = opening_balance - base_capital

# beacuse I am loosing money, so I have 0  market money, and I can take risk on the current opening balance and not on the base capital
if (market_money < 0):
	market_money = 0
	base_capital = opening_balance


market_money_risk   = (market_money*1)/100
base_capital_risk   = (base_capital*0.5)/100
max_risk_for_today  = base_capital_risk + market_money_risk


max_order_for_today  = 2
risk_per_trade       = (max_risk_for_today/max_order_for_today)
atr_multipler        = 3
risk_reward          = 3


watchlist            = ['NIFTY', 'ADANIPORTS', 'ADANIENT', 'SBIN']


single_order     = {'name':None, 'date':None , 'entry_time': None, 'entry_price': None, 'buy_sell': None, 'qty': None, 'sl': None, 'exit_time': None, 'exit_price': None, 'pnl': None, 'remark': None, 'traded':None}
orderbook        = {}
wb               = xw.Book('Live Trade Data.xlsx')
live_Trading     = wb.sheets['Live_Trading']
completed_orders_sheet = wb.sheets['completed_orders']
reentry          = "yes" #"yes/no"
completed_orders = []


bot_token        = "8059847390:AAECSnQK-yOaGJ-clJchb1cx8CDhx2VQq-M"
receiver_chat_id = "1918451082"



live_Trading.range("A2:Z100").value = None
completed_orders_sheet.range("A2:Z100").value = None

for name in watchlist:
	orderbook[name] = single_order.copy()





while True:

	print("starting while Loop \n\n")

	current_time = datetime.datetime.now().time()
	if current_time < datetime.time(10, 15):
		print(f"Wait for market to start", current_time)
		time.sleep(1)
		continue

	live_pnl = tsl.get_live_pnl()
	max_loss_hit = live_pnl < (max_risk_for_today*-1)
	market_over  = current_time > datetime.time(15, 15)

	if max_loss_hit or market_over:
		order_details = tsl.cancel_all_orders()
		print(f"Market over Closing all trades !! Bye Bye See you Tomorrow", current_time)
		pdb.set_trace()
		break

	all_ltp = tsl.get_ltp_data(names = watchlist)

	for name in watchlist:


		orderbook_df                       = pd.DataFrame(orderbook).T
		live_Trading.range('A1').value     = orderbook_df

		completed_orders_df                =  pd.DataFrame(completed_orders)
		completed_orders_sheet.range('A1').value = completed_orders_df


		current_time          = datetime.datetime.now()
		print(f"Scanning        {name} {current_time}")



		try:

			if name == "NIFTY":
				exchange = "INDEX"
			else:
				exchange = "NSE"

			chart                 = tsl.get_historical_data(tradingsymbol = name,exchange = exchange,timeframe="5")
			chart['rsi']          = talib.RSI(chart['close'], timeperiod=14)

			sqn_lib.sqn(df=chart, period=21)
			chart['market_type'] = chart['sqn'].apply(sqn_lib.market_type)

			chart['atr'] = talib.ATR(chart['high'], chart['low'], chart['close'], timeperiod=14)

			cc  = chart.iloc[-2]

			no_of_orders_placed = orderbook_df[orderbook_df['qty'] > 0].shape[0] + completed_orders_df[completed_orders_df['qty'] > 0].shape[0]



			# buy entry conditions
			bc1 = cc['rsi'] > 1
			bc2 = orderbook[name]['traded'] is None
			bc3 = True # cc['market_type'] != "neutral"
			bc4 = no_of_orders_placed < 5





		except Exception as e:
			print(e)
			continue



		if bc1 and bc2 and bc3:
			print("buy ", name, "\t")


			pdb.set_trace()


			# margin_avialable = tsl.get_balance()
			# margin_required  = cc['close']/4.5

			# if margin_avialable < margin_required:
			# 	print(f"Less margin, not taking order : margin_avialable is {margin_avialable} and margin_required is {margin_required} for {name}")
			# 	continue



			ce_name, pe_name, ce_otm_strike, pe_otm_strike = tsl.OTM_Strike_Selection(Underlying='NIFTY', Expiry=0, OTM_count=2)

			lot_size                          = tsl.get_lot_size(tradingsymbol = ce_name)
			options_chart                     = tsl.get_historical_data(tradingsymbol = ce_name,exchange = 'NFO',timeframe="5")
			options_chart['atr'] 			  = talib.ATR(options_chart['high'], options_chart['low'], options_chart['close'], timeperiod=14)
			rc_options                        = options_chart.iloc[-1]

			orderbook[name]['name']           = name
			orderbook[name]['options_name']   = ce_name

			orderbook[name]['date']           = str(current_time.date())
			orderbook[name]['entry_time']     = str(current_time.time())[:8]
			orderbook[name]['max_holding_time']   = datetime.datetime.now() + datetime.timedelta(hours=2)

			orderbook[name]['buy_sell']       = "BUY"
			sl_points                         = rc_options['atr']*atr_multipler
			orderbook[name]['qty']            = 25 # int(int((risk_per_trade*0.7)/sl_points)/lot_size)*lot_size


			try:
				entry_orderid                     = tsl.order_placement(tradingsymbol=orderbook[name]['options_name'] ,exchange='NFO', quantity=orderbook[name]['qty'], price=0, trigger_price=0, order_type='MARKET', transaction_type='BUY', trade_type='MIS')
				orderbook[name]['entry_orderid']  = entry_orderid
				orderbook[name]['entry_price']    = tsl.get_executed_price(orderid=orderbook[name]['entry_orderid'])

				orderbook[name]['sl']             = round(orderbook[name]['entry_price'] - sl_points, 1)    # 99
				orderbook[name]['tsl']            = orderbook[name]['sl']

				price                             = orderbook[name]['sl'] - 0.05



				sl_orderid                        = tsl.order_placement(tradingsymbol=orderbook[name]['options_name'] ,exchange='NFO', quantity=orderbook[name]['qty'], price=price, trigger_price=orderbook[name]['sl'], order_type='STOPLIMIT', transaction_type ='SELL', trade_type='MIS')
				orderbook[name]['sl_orderid']     = sl_orderid
				orderbook[name]['traded']         = "yes"


				message = "\n".join(f"'{key}': {repr(value)}" for key, value in orderbook[name].items())
				message = f"Entry_done {name} \n\n {message}"
				tsl.send_telegram_alert(message=message,receiver_chat_id=receiver_chat_id,bot_token=bot_token)



			except Exception as e:
				print(e)
				pdb.set_trace(header= "error in entry order")





		if orderbook[name]['traded'] == "yes":
			bought = orderbook[name]['buy_sell'] == "BUY"

			if bought:

				try:
					ltp       = all_ltp[name]
					sl_hit    = tsl.get_order_status(orderid=orderbook[name]['sl_orderid']) == "TRADED"

					holding_time_exceeded = datetime.datetime.now() > orderbook[name]['max_holding_time']
					current_pnl           = round((ltp - orderbook[name]['entry_price'])*orderbook[name]['qty'],1)


				except Exception as e:
					print(e)
					pdb.set_trace(header = "error in sl order cheking")



				if sl_hit:

					try:
						orderbook[name]['exit_time']  = str(current_time.time())[:8]
						orderbook[name]['exit_price'] = tsl.get_executed_price(orderid=orderbook[name]['sl_orderid'])
						orderbook[name]['pnl']        = round((orderbook[name]['exit_price'] - orderbook[name]['entry_price'])*orderbook[name]['qty'],1)
						orderbook[name]['remark']     = "Bought_SL_hit"

						message = "\n".join(f"'{key}': {repr(value)}" for key, value in orderbook[name].items())
						message = f"SL_HIT {name} \n\n {message}"
						tsl.send_telegram_alert(message=message,receiver_chat_id=receiver_chat_id,bot_token=bot_token)



						if reentry == "yes":
							completed_orders.append(orderbook[name])
							orderbook[name] = None
					except Exception as e:
						print(e)
						pdb.set_trace(header = "error in sl_hit")



				if holding_time_exceeded and (current_pnl < 0):

					try:
						tsl.cancel_order(OrderID=orderbook[name]['sl_orderid'])
						time.sleep(2)
						square_off_buy_order          = tsl.order_placement(tradingsymbol=orderbook[name]['name'] ,exchange='NSE', quantity=orderbook[name]['qty'], price=0, trigger_price=0,    order_type='MARKET',     transaction_type='SELL',   trade_type='MIS')

						orderbook[name]['exit_time']  = str(current_time.time())[:8]
						orderbook[name]['exit_price'] = tsl.get_executed_price(orderid=square_off_buy_order)
						orderbook[name]['pnl']        = (orderbook[name]['exit_price'] - orderbook[name]['entry_price'])*orderbook[name]['qty']
						orderbook[name]['remark']     = "holding_time_exceeded_and_I_am_still_facing_loss"

						message = "\n".join(f"'{key}': {repr(value)}" for key, value in orderbook[name].items())
						message = f"holding_time_exceeded_and_I_am_still_facing_loss {name} \n\n {message}"
						tsl.send_telegram_alert(message=message,receiver_chat_id=receiver_chat_id,bot_token=bot_token)


						if reentry == "yes":
							completed_orders.append(orderbook[name])
							orderbook[name] = None

						winsound.Beep(1500, 10000)

					except Exception as e:
						print(e)
						pdb.set_trace(header = "error in tg_hit")   # Testing changes. sadhasd ajsdas dbna sdb abs da sd asd abs d asd



				options_name                      = orderbook[name]['options_name']
				options_chart                     = tsl.get_historical_data(tradingsymbol = options_name,exchange = 'NFO',timeframe="5")
				options_chart['atr'] 			  = talib.ATR(options_chart['high'], options_chart['low'], options_chart['close'], timeperiod=14)
				rc_options                        = options_chart.iloc[-1]
				sl_points                         = rc_options['atr']*atr_multipler
				options_ltp                       = tsl.get_ltp_data(names = options_name)[options_name]
				tsl_level                         = options_ltp - sl_points

				if tsl_level > orderbook[name]['tsl']:
					trigger_price = round(tsl_level, 1)
					price         = trigger_price - 0.05
					tsl.modify_order(order_id=orderbook[name]['sl_orderid'],order_type="STOPLIMIT",quantity=25,price=price,trigger_price=trigger_price)
					orderbook[name]['tsl'] = tsl_level





# order_ids      = tsl.place_slice_order(tradingsymbol="NIFTY 19 DEC 24400 CALL",   exchange="NFO",quantity=10000, transaction_type="BUY",order_type="LIMIT",trade_type="MIS",price=0.05)




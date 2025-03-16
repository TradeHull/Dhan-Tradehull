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

client_code = "1102790337"
token_id    = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzM0NjczMzYzLCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMjc5MDMzNyJ9.CCf2zbKNXrwO-TfZZfs3fLfDkw8-RPGgKLCHQ7P4-AARE2i-P0OVyVFQUKPzymcgHS-Ux-zILrQ0_gAEMhGihQ"
tsl         = Tradehull(client_code,token_id)


watchlist   = ['NIFTY']




single_order           = {'name':None, 'date':None , 'entry_time': None, 'entry_price': None, 'buy_sell': None, 'qty': None, 'sl': None, 'exit_time': None, 'exit_price': None, 'pnl': None, 'remark': None, 'traded':None}
orderbook              = {}
wb                     = xw.Book('Live Trade Data.xlsx')
live_Trading           = wb.sheets['Live_Trading']
completed_orders_sheet = wb.sheets['completed_orders']
Combined_premium_graph = wb.sheets['Combined_premium_graph']

reentry                = "yes" #"yes/no"
completed_orders       = []


bot_token              = "8059847390:AAECSnQK-yOaGJ-clJchb1cx8CDhx2VQq-M"
receiver_chat_id       = "1918451082"


live_Trading.range("A2:Z100").value = None
completed_orders_sheet.range("A2:Z100").value = None

for name in watchlist:
	orderbook[name] = single_order.copy()



combined_premium_data = {}
Combined_premium_graph.range('A2:Z100000').value = None


while True:

	try:

		print("starting while Loop \n\n")

		current_time = datetime.datetime.now().time()
		if current_time < datetime.time(9, 20):
			print(f"Wait for market to start", current_time)
			time.sleep(1)
			continue

		if current_time > datetime.time(15, 15):
			order_details = tsl.cancel_all_orders()
			print(f"Market over Closing all trades !! Bye Bye See you Tomorrow", current_time)
			pdb.set_trace()
			break



		for name in watchlist:

			orderbook_df                             = pd.DataFrame(orderbook).T
			live_Trading.range('A1').value           = orderbook_df

			completed_orders_df                      =  pd.DataFrame(completed_orders)
			completed_orders_sheet.range('A1').value = completed_orders_df


			time.sleep(2)
			combined_premium_df                      = pd.DataFrame(combined_premium_data).T
			Combined_premium_graph.range('A1').value = combined_premium_df



			current_time          = datetime.datetime.now()
			print(f"Scanning        {name} {current_time}")


			bc2 = orderbook[name]['traded'] is None


			if bc2:
				print("Creating Entry Set ", name, "\t")


				try:
					atm_call_name, atm_put_name, strike = tsl.ATM_Strike_Selection(Underlying=name, Expiry=0)
					all_ltp_data = tsl.get_ltp_data(names=[atm_call_name, atm_put_name])

					if len(my_dict) == 0:
						continue

				except Exception as e:
					print(e)
					continue

				atm_call_ltp  = all_ltp_data[atm_call_name]
				atm_put_ltp   = all_ltp_data[atm_put_name]
				combined_premium = atm_call_ltp + atm_put_ltp
				distance_for_otm = int(combined_premium/50) + 1




				otm_ce_name, otm_pe_name, ce_OTM_strike, pe_OTM_strike = tsl.OTM_Strike_Selection(Underlying=name, Expiry=0, OTM_count=distance_for_otm)

				# Entry set
				orderbook[name]['qty']            = tsl.get_lot_size(tradingsymbol = otm_ce_name)

				buy_otm_pe_orderid  = tsl.order_placement(tradingsymbol=otm_pe_name ,  exchange='NFO', quantity=orderbook[name]['qty'], price=0, trigger_price=0, order_type='MARKET', transaction_type='BUY', trade_type='MIS')
				time.sleep(0.25)

				buy_otm_ce_orderid  = tsl.order_placement(tradingsymbol=otm_ce_name ,  exchange='NFO', quantity=orderbook[name]['qty'], price=0, trigger_price=0, order_type='MARKET', transaction_type='BUY', trade_type='MIS')
				time.sleep(0.25)

				sell_atm_ce_orderid = tsl.order_placement(tradingsymbol=atm_call_name ,exchange='NFO', quantity=orderbook[name]['qty'], price=0, trigger_price=0, order_type='MARKET', transaction_type='SELL', trade_type='MIS')
				time.sleep(0.25)

				sell_atm_pe_orderid = tsl.order_placement(tradingsymbol=atm_put_name , exchange='NFO', quantity=orderbook[name]['qty'], price=0, trigger_price=0, order_type='MARKET', transaction_type='SELL', trade_type='MIS')
				time.sleep(0.25)


				orderbook[name]['otm_pe_name']   =  otm_pe_name
				orderbook[name]['otm_ce_name']   =  otm_ce_name
				orderbook[name]['atm_call_name'] =  atm_call_name
				orderbook[name]['atm_put_name']  =  atm_put_name


				orderbook[name]['buy_otm_pe_orderid']   =  buy_otm_pe_orderid
				orderbook[name]['buy_otm_ce_orderid']   =  buy_otm_ce_orderid
				orderbook[name]['sell_atm_ce_orderid']  =  sell_atm_ce_orderid
				orderbook[name]['sell_atm_pe_orderid']  =  sell_atm_pe_orderid


				orderbook[name]['name']           = name
				orderbook[name]['date']           = str(current_time.date())
				orderbook[name]['entry_time']     = str(current_time.time())[:8]


				orderbook[name]['combined_premium'] = combined_premium
				orderbook[name]['tg']               = combined_premium*0.80
				orderbook[name]['sl']               = combined_premium*1.20
				orderbook[name]['traded']           = "yes"


				combined_premium_data[str(current_time)]  = {"combined_premium":combined_premium, "combined_premium_sl":combined_premium*1.15, "combined_premium_tg":combined_premium*0.7}



				message = "\n".join(f"'{key}': {repr(value)}" for key, value in orderbook[name].items())
				message = f"Entry_done {name} \n\n {message}"
				tsl.send_telegram_alert(message=message,receiver_chat_id=receiver_chat_id,bot_token=bot_token)





			if orderbook[name]['traded'] == "yes":


				otm_pe_name   =  orderbook[name]['otm_pe_name']
				otm_ce_name   =  orderbook[name]['otm_ce_name']
				atm_call_name = orderbook[name]['atm_call_name']
				atm_put_name  = orderbook[name]['atm_put_name']



				try:
					all_ltp_data  = tsl.get_ltp_data(names=[atm_call_name, atm_put_name])

					if len(my_dict) == 0:
						continue

				except Exception as e:
					print(e)
					continue


				running_combined_premium = all_ltp_data[atm_call_name] + all_ltp_data[atm_put_name]
				combined_premium_data[str(current_time)]  = {"combined_premium":running_combined_premium, "combined_premium_sl":orderbook[name]['sl'], "combined_premium_tg":orderbook[name]['tg']}


				sl_hit    = running_combined_premium > orderbook[name]['sl']
				tg_hit    = running_combined_premium < orderbook[name]['tg']


				if sl_hit or tg_hit:

					sell_otm_pe_orderid  = tsl.order_placement(tradingsymbol=otm_pe_name ,  exchange='NFO', quantity=orderbook[name]['qty'], price=0, trigger_price=0, order_type='MARKET', transaction_type='SELL', trade_type='MIS')
					time.sleep(0.25)

					sell_otm_ce_orderid  = tsl.order_placement(tradingsymbol=otm_ce_name ,  exchange='NFO', quantity=orderbook[name]['qty'], price=0, trigger_price=0, order_type='MARKET', transaction_type='SELL', trade_type='MIS')
					time.sleep(0.25)

					buy_atm_ce_orderid   = tsl.order_placement(tradingsymbol=atm_call_name ,exchange='NFO', quantity=orderbook[name]['qty'], price=0, trigger_price=0, order_type='MARKET', transaction_type='BUY', trade_type='MIS')
					time.sleep(0.25)

					buy_atm_pe_orderid   = tsl.order_placement(tradingsymbol=atm_put_name , exchange='NFO', quantity=orderbook[name]['qty'], price=0, trigger_price=0, order_type='MARKET', transaction_type='BUY', trade_type='MIS')
					time.sleep(0.25)


					message = "\n".join(f"'{key}': {repr(value)}" for key, value in orderbook[name].items())
					message = f"SET EXITED {name} \n\n {message}"
					tsl.send_telegram_alert(message=message,receiver_chat_id=receiver_chat_id,bot_token=bot_token)


					if reentry == "yes":
						completed_orders.append(orderbook[name])
						orderbook[name] = {'name':None, 'date':None , 'entry_time': None, 'entry_price': None, 'buy_sell': None, 'qty': None, 'sl': None, 'exit_time': None, 'exit_price': None, 'pnl': None, 'remark': None, 'traded':None}
						Combined_premium_graph.range('A2:Z100000').value = None

	except Exception as e:
		print(e)
		continue

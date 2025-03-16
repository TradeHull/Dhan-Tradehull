# https://ta-lib.github.io/ta-lib-python/
# https://www.notion.so/TradeHull-Dhan-Codebase-76b32fa814e64aea843e14a148854214#efa40986725341e6bfa9ad6fcfc10a6d

import pdb
from Dhan_Tradehull_V2 import Tradehull
import pandas as pd
import talib
import time
import datetime

client_code = ""
token_id    = ""
tsl = Tradehull(client_code,token_id)

available_balance = tsl.get_balance()
leveraged_margin  = available_balance*5
max_trades = 1
per_trade_margin = (leveraged_margin/max_trades)
max_loss = (available_balance*1)/100*-1

watchlist = ['NIFTY']

initial_entry_created = "no"
do_I_want_reentry = "yes"


while True:

	live_pnl = tsl.get_live_pnl()
	current_time = datetime.datetime.now().time()

	if current_time < datetime.time(9, 20):
		print("wait for market to start", current_time)
		continue

	if (current_time > datetime.time(23, 15)) or (live_pnl < max_loss):
		I_want_to_trade_no_more = tsl.kill_switch('ON')
		order_details = tsl.cancel_all_orders()
		print("Market is over, Bye Bye see you tomorrow", current_time)
		break

	for stock_name in watchlist:
		time.sleep(0.2)
		print(stock_name)

		# Make Initial Entry
		if initial_entry_created == "no":
			atm_ce_name, atm_pe_name, strike = tsl.ATM_Strike_Selection(Underlying=stock_name, Expiry=0)
			data = tsl.get_ltp_data(names = [atm_ce_name,atm_pe_name])
			atm_ce_ltp     = data[atm_ce_name]
			atm_pe_ltp     = data[atm_pe_name]
			lot_size       = tsl.get_lot_size(atm_ce_name)

			ce_orderid = tsl.order_placement(atm_ce_name,'NFO',lot_size, 0, 0, 'MARKET', 'SELL', 'MIS')
			pe_orderid = tsl.order_placement(atm_pe_name,'NFO',lot_size, 0, 0, 'MARKET', 'SELL', 'MIS')

			combined_premium_received = atm_ce_ltp + atm_pe_ltp
			combined_sl_premium       = combined_premium_received*1.2
			initial_entry_created     = "yes_I_have_shorted_straddle"


		# check for Stoploss
		if initial_entry_created == "yes_I_have_shorted_straddle":
			data = tsl.get_ltp_data(names = [atm_ce_name,atm_pe_name])			
			atm_ce_ltp     = data[atm_ce_name]
			atm_pe_ltp     = data[atm_pe_name]

			running_combined_premium = atm_ce_ltp + atm_pe_ltp

			if running_combined_premium > combined_sl_premium:
				ce_orderid = tsl.order_placement(atm_ce_name,'NFO',lot_size, 0, 0, 'MARKET', 'BUY', 'MIS')
				pe_orderid = tsl.order_placement(atm_pe_name,'NFO',lot_size, 0, 0, 'MARKET', 'BUY', 'MIS')

				if do_I_want_reentry == "yes":
					initial_entry_created = "no"

				if do_I_want_reentry == "no":
					I_want_to_trade_no_more = tsl.kill_switch('ON')
					order_details = tsl.cancel_all_orders()
					break







# https://ta-lib.github.io/ta-lib-python/
# https://www.notion.so/TradeHull-Dhan-Codebase-76b32fa814e64aea843e14a148854214#efa40986725341e6bfa9ad6fcfc10a6d


import pdb
from Dhan_Tradehull_V2 import Tradehull
import pandas as pd
import talib
import time
import datetime

client_code = "1102790337"
token_id    = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzM0MDcxMzE5LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMjc5MDMzNyJ9.4i-edsCp4Z2r6Z82ewoZFW_enhENZ_4p1IdJcED5fROHGiqSqy_3yglYblDKlWIJIM8S9VM4ZwXfqd3T0ZfVZg"


tsl = Tradehull(client_code,token_id)



available_balance = tsl.get_balance()
leveraged_margin  = available_balance*5
max_trades = 1
per_trade_margin = (leveraged_margin/max_trades)
max_loss = (available_balance*1)/100*-1

watchlist = ['BRITANNIA']
traded_wathclist = []
tarde_info = {'Direction': 'buy', 'level': 5921.0}


while True:

	live_pnl = tsl.get_live_pnl()
	current_time = datetime.datetime.now().time()

	if current_time < datetime.time(9, 30):
		print("wait for market to start", current_time)
		continue

	if (current_time > datetime.time(15, 15)) or (live_pnl < max_loss):
		# I_want_to_trade_no_more = tsl.kill_switch('ON')   # removed Kill swtich as it may get accidenyl hit while Testing and block all future order placement
		order_details = tsl.cancel_all_orders()
		print("Market is over, Bye Bye see you tomorrow", current_time)
		break

	for stock_name in watchlist:
		time.sleep(0.2)
		print(f"Scaning {stock_name}")


		chart_5            = tsl.get_historical_data(tradingsymbol = stock_name, exchange = 'NSE',timeframe="5")       # Upgraded 5 minute chart according to Dhan_Tradehull_V2
		cc_5               = chart_5.iloc[-1]   # pandas
		no_repeat_order    = stock_name not in traded_wathclist


		if (tarde_info['Direction'] == "buy") and no_repeat_order:
			cc_volume      = cc_5['volume']
			average_volume = chart_5['volume'].mean()

			breakout_c1    = cc_5['close'] > tarde_info['level']
			breakout_c2    = cc_volume > 2*average_volume
			breakout_c3    = cc_5['open'] != cc_5['close']

			atm_ce_name, atm_pe_name, strike = tsl.ATM_Strike_Selection(stock_name,'28-11-2024')  #atm_ce_name, pe_strike, ce_OTM_price, pe_OTM_price = tsl.OTM_Strike_Selection(stock_name,'08-08-2024',3)


			atm_ce_ltp     = tsl.get_ltp_data(names = [atm_ce_name])[atm_ce_name]
			lot_size       = tsl.get_lot_size(atm_ce_name)
			entry_price    = round((atm_ce_ltp*1.02),1)

			sl_price       = round((atm_ce_ltp*0.8),1)


			entry_orderid  = tsl.order_placement(atm_ce_name,'NFO', lot_size, entry_price, 0, 'LIMIT', 'BUY', 'MIS')
			sl_orderid     = tsl.order_placement(atm_ce_name,'NFO', lot_size, 0, sl_price, 'STOPMARKET', 'SELL', 'MIS')

			traded_wathclist.append(stock_name)







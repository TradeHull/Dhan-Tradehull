import pdb
import time
import datetime
import traceback
import talib
from Dhan_Tradehull import Tradehull
import pandas as pd


client_code = "1102790337"
token_id = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzI1NDMxNTc2LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMjc5MDMzNyJ9.sW4kUgmS2WS7RX24OqPF07vkAdiQko3ZAX3dsKeBu_SzHio_yUQjla4PPp9TbDEwzn8pw1MH1nh4MvHjb7MZ_g"
tsl = Tradehull(client_code,token_id) # tradehull_support_library

tsl.get_intraday_data('ACC','NSE',1)

tsl.get_intraday_data('NIFTY','NSE',1)


available_balance = tsl.get_balance()
max_risk_for_the_day = (available_balance*1)/100*-1
print("available_balance", available_balance)

ltp1 = tsl.get_ltp('ACC')
ltp2 = tsl.get_ltp('NIFTY')
ltp3 = tsl.get_ltp('BANKNIFTY 28 AUG 51600 CALL')
ltp4 = tsl.get_ltp('NIFTY 29 AUG 23200 CALL')

previous_hist_data = tsl.get_historical_data('ACC','NSE',12)
intraday_hist_data = tsl.get_intraday_data('ACC','NSE',1)



ce_name, pe_name, strike = tsl.ATM_Strike_Selection('NIFTY','05-09-2024')
otm_ce_name, pe_name, ce_OTM_strike, pe_OTM_strike = tsl.OTM_Strike_Selection('NIFTY','05-09-2024',3)
ce_name, pe_name, ce_ITM_strike, pe_ITM_strike = tsl.ITM_Strike_Selection('NIFTY','05-09-2024', 4)


intraday_hist_data = tsl.get_intraday_data(otm_ce_name,'NFO',1)
intraday_hist_data['rsi'] = talib.RSI(intraday_hist_data['close'], timeperiod=14)


lot_size = tsl.get_lot_size('NIFTY 29 AUG 24500 CALL')
lot_size = tsl.get_lot_size(otm_ce_name)
qty = 2*lot_size

# next lecture
orderid1 = tsl.order_placement('NIFTY 29 AUG 24500 CALL','NFO',25, 0.05, 0, 'LIMIT', 'BUY', 'MIS')
orderid2 = tsl.order_placement('BANKNIFTY 28 AUG 51600 CALL','NFO',15, 0.05, 0, 'LIMIT', 'BUY', 'MIS')
orderid3 = tsl.order_placement('ACC','NSE', 1, 0, 0, 'MARKET', 'BUY', 'MIS')
exit_all = tsl.cancel_all_orders()
















live_pnl = tsl.get_live_pnl()
if live_pnl < max_risk_for_the_day:
	exit_all = tsl.cancel_all_orders()
	response = tsl.kill_switch('ON')





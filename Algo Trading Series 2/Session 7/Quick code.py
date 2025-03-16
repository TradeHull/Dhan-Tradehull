import pdb
import time
import datetime
import traceback
from Dhan_Tradehull import Tradehull
import pandas as pd
from pprint import pprint
import talib


client_code = "1102790337"
token_id    = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzM1NTQ3ODE5LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMjc5MDMzNyJ9.xC4uOx0WmfKHjjNJbSWLsGWj3Aubuko47tnsBw-QlVQTcGkrBtnHwPPIDv0Hth3tbg96CyFtSHnGmy1ogB9eaQ"
tsl         = Tradehull(client_code,token_id)

pdb.set_trace()
chart = tsl.get_historical_data(tradingsymbol = 'NIFTY',exchange = 'INDEX',timeframe="5")

ltp   = tsl.get_ltp_data(names = ['NIFTY 05 DEC 24000 CALL', 'NIFTY 05 DEC 24000 PUT'])
data  = tsl.get_historical_data(tradingsymbol = 'ACC'     ,exchange = 'NSE'  ,timeframe="15")



order_details = tsl.get_order_detail(orderid=102241104416927)
order_status  = tsl.get_order_status(orderid=102241104416927)
order_price   = tsl.get_executed_price(orderid=102241104416927)
order_time    = tsl.get_exchange_time(orderid=102241104416927)


positions = tsl.get_positions()
orderbook = tsl.get_orderbook()
tradebook = tsl.get_trade_book()
holdings = tsl.get_holdings()


ce_strike, pe_strike, strike = tsl.ATM_Strike_Selection(Underlying='NIFTY', Expiry=0)


ce_strike, pe_strike, ce_OTM_price, pe_OTM_price = tsl.OTM_Strike_Selection(Underlying='NIFTY', Expiry=0, OTM_count=5)

ce_strike, pe_strike, ce_OTM_price, pe_OTM_price = tsl.ITM_Strike_Selection(Underlying='NIFTY', Expiry=0, OTM_count=5)

# Equity
entry_orderid  = tsl.order_placement(tradingsymbol='ACC' ,exchange='NSE', quantity=1, price=0, trigger_price=0,    order_type='MARKET',     transaction_type='BUY',   trade_type='MIS')
sl_orderid     = tsl.order_placement(tradingsymbol='ACC' ,exchange='NSE', quantity=1, price=0, trigger_price=2200, order_type='STOPMARKET', transaction_type ='SELL', trade_type='MIS')

# Options
entry_orderid  = tsl.order_placement(tradingsymbol='NIFTY 19 DEC 24400 CALL' ,exchange='NFO', quantity=25, price=0, trigger_price=0, order_type='MARKET', transaction_type='BUY', trade_type='MIS')
sl_orderid     = tsl.order_placement(tradingsymbol='NIFTY 19 DEC 24400 CALL' ,exchange='NFO', quantity=25, price=25, trigger_price=30, order_type='STOPLIMIT', transaction_type='SELL', trade_type='MIS')


modified_order = tsl.modify_order(order_id=sl_orderid,order_type="STOPLIMIT",quantity=25,price=price,trigger_price=trigger_price)
order_ids      = tsl.place_slice_order(tradingsymbol="NIFTY 19 DEC 24400 CALL",   exchange="NFO",quantity=5000, transaction_type="BUY",order_type="LIMIT",trade_type="MIS",price=0.05)



margin = tsl.margin_calculator(tradingsymbol='ACC', exchange='NSE', transaction_type='BUY', quantity=2, trade_type='MIS', price=2180, trigger_price=0)
margin = tsl.margin_calculator(tradingsymbol='NIFTY 19 DEC 24400 CALL', exchange='NFO', transaction_type='SELL', quantity=25, trade_type='MARGIN', price=43, trigger_price=0)
margin = tsl.margin_calculator(tradingsymbol='NIFTY 19 DEC 24400 CALL', exchange='NFO', transaction_type='BUY', quantity=25, trade_type='MARGIN', price=43, trigger_price=0)
margin = tsl.margin_calculator(tradingsymbol='NIFTY DEC FUT', exchange='NFO', transaction_type='BUY', quantity=25, trade_type='MARGIN', price=24350, trigger_price=0)


exit_all       = tsl.cancel_all_orders()





import pandas_ta as ta

index_chart['rsi'] = talib.RSI(index_chart['close'], timeperiod=14)

index_chart.set_index(pd.DatetimeIndex(index_chart['timestamp']), inplace=True)
index_chart['vwap'] = pta.vwap(index_chart['high'] , index_chart['low'], index_chart['close'] , index_chart['volume'])

indi = ta.supertrend(index_chart['high'], index_chart['low'], index_chart['close'], 10, 2)
index_chart = pd.concat([index_chart, indi], axis=1, join='inner')


index_chart['pv'] = index_chart['close'] * index_chart['volume']
index_chart['vwma'] = index_chart['pv'].rolling(20).mean() / index_chart['volume'].rolling(20).mean()











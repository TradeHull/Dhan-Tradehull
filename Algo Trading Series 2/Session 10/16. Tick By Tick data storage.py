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


wb                     = xw.Book('Live Trade Data.xlsx')
data_storage           = wb.sheets['Data Storage']

bot_token              = "8059847390:AAECSnQK-yOaGJ-clJchb1cx8CDhx2VQq-M"
receiver_chat_id       = "1918451082"


ce_strike, pe_strike, strike = tsl.ATM_Strike_Selection(Underlying='NIFTY', Expiry=0)

all_strike   = [strike + number*50 for number in range(-20, 20)]
all_ce_names = ["NIFTY 26 DEC " + str(strike) + " CALL" for strike in all_strike]
all_pe_names = ["NIFTY 26 DEC " + str(strike) + " PUT" for strike in all_strike]
equity_names = ["ACC", "CIPLA", "GAIL", "NIFTY"]

all_names = all_ce_names + all_pe_names + equity_names




data_storage.range('B1').value = all_names



for row_no in range(2, 1000000):


	try:
		current_time = datetime.datetime.now()
		print(current_time)


		if current_time.second % 5 == 0:
			tsl.send_telegram_alert(message=f"{current_time} data storage is working fine ",receiver_chat_id=receiver_chat_id,bot_token=bot_token)


		all_ltp   = tsl.get_ltp_data(names = all_names)

		temp_dict = {}
		temp_dict[current_time] = all_ltp

		temp_dict = pd.DataFrame(temp_dict)

		ltp_sequence = temp_dict.T[all_names].iloc[0].to_list()


		data_storage.range('B' + str(row_no)).value = ltp_sequence
		data_storage.range('A' + str(row_no)).value = str(current_time)

	except Exception as e:
		print(e)
		tsl.send_telegram_alert(message="error in storing data",receiver_chat_id=receiver_chat_id,bot_token=bot_token)
		continue

















# get_call_and_put_names = 

# all_ltp_data =

# store ltp = 














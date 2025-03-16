import pdb
import time
import datetime
import traceback
from Dhan_Tradehull import Tradehull
import pandas as pd
from pprint import pprint
import talib
import xlwings as xw
import time

client_code = "1102790337"
token_id    = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzM1NTQ3ODE5LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMjc5MDMzNyJ9.xC4uOx0WmfKHjjNJbSWLsGWj3Aubuko47tnsBw-QlVQTcGkrBtnHwPPIDv0Hth3tbg96CyFtSHnGmy1ogB9eaQ"
tsl         = Tradehull(client_code,token_id)

# wb     = xw.Book('Live Option Chain.xlsx')
# sheet  = wb.sheets['Sheet1']

# bot_token        = "8059847390:AAECSnQK-yOaGJ-clJchb1cx8CDhx2VQq-M"
# receiver_chat_id = "1918451082"


# message          = "Good afternoon"



# tsl.send_telegram_alert(message=message,receiver_chat_id=receiver_chat_id,bot_token=bot_token)







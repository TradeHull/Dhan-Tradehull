import xlwings as xw
import pdb
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

wb     = xw.Book('I want to talk to you.xlsx')
sheet  = wb.sheets['Sheet1']
sheet2 = wb.sheets['Sheet2']


chart = tsl.get_historical_data(tradingsymbol = 'NIFTY',exchange = 'INDEX',timeframe="5")


sheet2.range('A1').value = 



pdb.set_trace()



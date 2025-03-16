from Dhan_Tradehull import Tradehull
import datetime
import pdb
import os



client_code = "1102846586"
token_id = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzM1MTE0MTkxLCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMjg0NjU4NiJ9.fCoeEhQ6Q2qn2rnhfm_1mKQ56vXLilQmFBaLXS8vzfexCEvSMJVpodJHhrMwcW2j60890de0n96wCwIsPdgRfg"
tsl = Tradehull(client_code, token_id)

index_name = 'NIFTY'

no_strikes_to_replay = 20

expiry_date = "19 DEC"

start_time ='2024-12-19 09:15:00+05:30'



today_date = datetime.datetime.now().date()

index_data = tsl.get_historical_data(tradingsymbol=index_name, exchange='INDEX', timeframe="1")

ATM_time_data = index_data[index_data['timestamp']==start_time]

if not ATM_time_data.empty:
    ATM_close = ATM_time_data.iloc[-1]['close']

step = tsl.index_step_dict[index_name]

ATM_Strike = round(ATM_close/step)*step

all_strikes = [ATM_Strike+(step*i) for i in range(1,no_strikes_to_replay+1)] + [ATM_Strike-(step*i) for i in range(1,no_strikes_to_replay+1)] + [ATM_Strike]

call_and_put_Strikes = [f"{index_name} {expiry_date} {strike} CALL" for strike in all_strikes] + [f"{index_name} {expiry_date} {strike} PUT" for strike in all_strikes]


file_path = f'data/{index_name}/{today_date}/'

directory = os.path.dirname(file_path)

if not os.path.exists(directory):
    os.makedirs(directory)

for strike in call_and_put_Strikes:
    option_df = tsl.get_historical_data(tradingsymbol=strike, exchange='NFO', timeframe="1")
    option_df.to_csv(f'data/{index_name}/{today_date}/{strike}.csv',index=False)





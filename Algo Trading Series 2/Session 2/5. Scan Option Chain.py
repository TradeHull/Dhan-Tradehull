import pdb
import time
import datetime
import traceback
from Dhan_Tradehull import Tradehull
import pandas as pd
from pprint import pprint
import talib
import pandas_ta as ta


client_code = "1102790337"
token_id    = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzM1NTQ3ODE5LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMjc5MDMzNyJ9.xC4uOx0WmfKHjjNJbSWLsGWj3Aubuko47tnsBw-QlVQTcGkrBtnHwPPIDv0Hth3tbg96CyFtSHnGmy1ogB9eaQ"
tsl         = Tradehull(client_code,token_id)




pdb.set_trace()

atm_strike, option_chain = tsl.get_option_chain(Underlying="NIFTY", exchange="INDEX", expiry=1,num_strikes=50)

# select that strike that has ltp less than rs 40.. on a lower level


# CE
striks_less_than_40         = option_chain[option_chain['CE LTP'] < 40]
index_of_my_required_strike = striks_less_than_40['CE LTP'].idxmax()
required_strike             = striks_less_than_40.loc[index_of_my_required_strike]['Strike Price']


# PE
striks_less_than_x          = option_chain[option_chain['PE LTP'] > 20]
index_of_my_required_strike = striks_less_than_x['PE LTP'].idxmin()
required_strike             = striks_less_than_x.loc[index_of_my_required_strike]['Strike Price']


sorted_oc       = option_chain.sort_values(by="CE Volume")
required_strike = sorted_oc.iloc[-1]


sorted_oc       = option_chain.sort_values(by="CE OI")
required_strike = sorted_oc.iloc[-1]


atm_stike_data   = option_chain[option_chain['Strike Price'] == atm_strike].iloc[0]
atm_stike_ce_oi  = atm_stike_data['CE OI']
atm_stike_pe_oi  = atm_stike_data['PE OI']




# volume pcr
pe_volume_sum  = option_chain['PE Volume'].sum()
ce_volume_sum  = option_chain['CE Volume'].sum()
volume_pcr = (pe_volume_sum/ce_volume_sum)



# oi pcr
pe_oi_sum  = option_chain['CE OI'].sum()
ce_oi_sum  = option_chain['PE OI'].sum()
oi_pcr     = (pe_oi_sum/ce_oi_sum)

import pdb
from Dhan_Tradehull import Tradehull


client_code = "1102790337"
token_id = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzI1NDMxNTc2LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMjc5MDMzNyJ9.sW4kUgmS2WS7RX24OqPF07vkAdiQko3ZAX3dsKeBu_SzHio_yUQjla4PPp9TbDEwzn8pw1MH1nh4MvHjb7MZ_g"
tsl = Tradehull(client_code,token_id)


# pdb.set_trace()

for distance_from_atm in range(1, 11):
	otm_ce_name, otm_pe_name, ce_OTM_strike, pe_OTM_strike = tsl.OTM_Strike_Selection('FINNIFTY','22-10-2024',distance_from_atm)
	ce_ltp = tsl.get_ltp(otm_ce_name)


	bc1 = (ce_ltp <= 5)

	if bc1:
		print("Found the strike which has less than Rs 5 Ltp" ,otm_ce_name, ce_ltp)
		break



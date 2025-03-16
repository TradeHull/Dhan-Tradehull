import pdb
from Dhan_Tradehull import Tradehull

client_code = "1102790337"
token_id = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzMxNDc5MTg1LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMjc5MDMzNyJ9.cJFmav3LOCQqz9Tp-KRJFPEYR-1Ds3G9YiZqXxcTfnQ3Nqgi4JJNd-y4XRbhfQD5RFAVLooTfZzpUGGstaLYLw"
tsl = Tradehull(client_code,token_id)

for distance_from_atm in range(1, 11):

	otm_ce_name, otm_pe_name, ce_OTM_strike, pe_OTM_strike = tsl.OTM_Strike_Selection('FINNIFTY','22-10-2024',distance_from_atm)
	ce_ltp = tsl.get_ltp(otm_ce_name)

	bc1 = (ce_ltp < 5)
	print(distance_from_atm, otm_ce_name, ce_ltp)

	if bc1:
		print("Found the strike which has less than Rs 5 Ltp" ,otm_ce_name, ce_ltp)



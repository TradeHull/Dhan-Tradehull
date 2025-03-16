import pandas as pd
import pdb


rsi_s              = [7,14,21, 28]
atr_sl_s           = [1,2, 3,4]
st_timepeiod_s     = [7,14,21, 28]
st_multipler_s     = [1,2, 3,4]
entry_time_s       = ["9:15", "10:15", "13:00", "14:00"]
timeframe_s        = [5,15,30, 60, "1day"]
position_sizing_s  = ["VBPS", "FIXD", "PCT"]
exit_method_s      = ["trail", "1_2", "1_3", "1_4"]


all_combinations = []

for rsi in rsi_s:
	for atr_sl in atr_sl_s:
		for st_timepeiod in st_timepeiod_s:
			for st_multipler in st_multipler_s:
				for entry_time in entry_time_s:
					for timeframe in timeframe_s:
						for position_sizing in position_sizing_s:
							for exit_method in exit_method_s:
								data = {"rsi":rsi, "atr_sl":atr_sl, "st_timepeiod":st_timepeiod, "st_multipler":st_multipler, "entry_time":entry_time, "timeframe":timeframe, "position_sizing":position_sizing, "exit_method":exit_method}
								all_combinations.append(data)



pdb.set_trace()




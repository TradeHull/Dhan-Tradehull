import pandas as pd
import datetime
import pdb
import os
import xlwings as xw
import time

index_name = 'NIFTY'
today_date = datetime.datetime.now().date()
directory = f'data/{index_name}/{today_date}/'
start_time ='2024-12-19 09:15:00+05:30'

wb  = xw.Book('Live_Option_Chain.xlsx')
sht = wb.sheets['Sheet1']


if os.path.exists(directory):
    csv_files = [file for file in os.listdir(directory) if file.endswith('.csv')]

df_list = []

for file in csv_files:

    file_path = f"{directory}{file}"  # Full file path
    df_close = pd.read_csv(file_path, usecols=['timestamp', 'close'], index_col='timestamp')
    new_close_name = file.split(" ")[3] + "_" + file.split(" ")[4][:-4]

    df_close.rename({"close": new_close_name}, axis='columns', inplace =True)
    df_list.append(df_close)




merged_df = pd.concat(df_list, axis=1, join='outer')
merged_df.fillna(method='ffill', inplace=True)


all_strikes = [x for x in set([x.split(" ")[3] for x in csv_files])]
all_strikes.sort()
merged_df = merged_df[start_time:]



sht.range('F2').expand('down').value = [[x] for x in all_strikes]


for timestamp, options_data in merged_df.iterrows():


    pdb.set_trace()
    

    Pause = sht.range('M3').value
    Speed = sht.range('M4').value

    time.sleep(Speed)


    if Pause == "yes":
        while True:
            Pause = sht.range('M3').value
            if Pause is None:
                break



    call_rows = [x + '_CALL' for x in all_strikes]
    call_ltp = options_data[call_rows]

    put_rows = [x + '_PUT' for x in all_strikes]
    put_ltp = options_data[put_rows]

    sht.range('E2').expand('down').value = [[x] for x in call_ltp.to_list()]
    sht.range('G2').expand('down').value = [[x] for x in put_ltp.to_list()]

    sht.range('M2').value = timestamp





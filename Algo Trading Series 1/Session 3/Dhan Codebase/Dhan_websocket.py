import datetime
import warnings
from dhanhq import marketfeed
import xlwings as xw
import pandas as pd
import time
import os

warnings.filterwarnings("ignore")

def get_instrument_file():
    global instrument_df
    current_date = time.strftime("%Y-%m-%d")
    expected_file = 'all_instrument ' + str(current_date) + '.csv'
    for item in os.listdir("Dependencies"):
        path = os.path.join(item)

        if (item.startswith('all_instrument')) and (current_date not in item.split(" ")[1]):
            if os.path.isfile("Dependencies\\" + path):
                os.remove("Dependencies\\" + path)

    if expected_file in os.listdir("Dependencies"):
        try:
            print(f"Reading existing file {expected_file}")
            instrument_df = pd.read_csv("Dependencies\\" + expected_file, low_memory=False)
        except Exception as e:
            print("This BOT Is Instrument file is not generated completely, Picking New File from Dhan Again")
            instrument_df = pd.read_csv("https://images.dhan.co/api-data/api-scrip-master.csv", low_memory=False)
            instrument_df.to_csv("Dependencies\\" + expected_file)
    else:
        # This will fetch instrument_df file from Dhan
        print("This BOT Is Picking New File From Dhan")
        instrument_df = pd.read_csv("https://images.dhan.co/api-data/api-scrip-master.csv", low_memory=False)
        instrument_df.to_csv("Dependencies\\" + expected_file)
    return instrument_df

# Excel sheet setup
wb = xw.Book("Websocket.xlsx")
sheet = wb.sheets['LTP']
client_id = "1102790337"
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzMxNDc5MTg1LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMjc5MDMzNyJ9.cJFmav3LOCQqz9Tp-KRJFPEYR-1Ds3G9YiZqXxcTfnQ3Nqgi4JJNd-y4XRbhfQD5RFAVLooTfZzpUGGstaLYLw"
# Fetch the instrument file
current_date = time.strftime("%Y-%m-%d")
expected_file = 'all_instrument ' + str(current_date) + '.csv'
global instrument_df, old_instruments
old_instruments = list()
instrument_df = get_instrument_file()

def create_instruments(watchlist, stock_exchange):
    rows = dict()
    row = 1
    instruments = list()
    instrument_exchange = {'NSE': "NSE", 'BSE': "BSE", 'NFO': 'NSE', 'BFO': 'BSE', 'MCX': 'MCX', 'CUR': 'NSE', 'BSE_IDX': 'BSE', 'NSE_IDX': 'NSE'}
    exchange_id = {'NSE': marketfeed.NSE, 'BSE': marketfeed.BSE, 'MCX': marketfeed.MCX, 'NFO': marketfeed.NSE_FNO, 'BFO': marketfeed.BSE_FNO, 'IDX': marketfeed.IDX, 'BSE_IDX': marketfeed.IDX, 'NSE_IDX': marketfeed.IDX}

    for tradingsymbol in watchlist:
        try:
            row += 1
            exchange_ = stock_exchange[tradingsymbol]
            exchange = instrument_exchange[exchange_]
            security_id = instrument_df[
                ((instrument_df['SEM_TRADING_SYMBOL'] == tradingsymbol) | (instrument_df['SEM_CUSTOM_SYMBOL'] == tradingsymbol)) &
                (instrument_df['SEM_EXM_EXCH_ID'] == instrument_exchange[exchange])
            ].iloc[-1]['SEM_SMST_SECURITY_ID']
            exchange_segment = exchange_id[exchange_]
            # Subscribe to Quote mode for now, can be changed to Ticker or Depth as needed
            instruments.append((exchange_segment, str(security_id), marketfeed.Quote))
            rows[security_id] = row
        except Exception as e:
            print(f"Error: {e} for {tradingsymbol}")
            continue

    return instruments, rows

def run_feed(client_id, access_token, instruments):
    try:
        # Initialize DhanFeed
        data = marketfeed.DhanFeed(client_id, access_token, instruments)
        previous_watchlist = []
        rows = {}
        old_instruments = instruments

        while True:
            # Check for updated watchlist
            last_row_col1 = sheet.range('A1').end('down').row
            last_row_col2 = sheet.range('B1').end('down').row
            row = max(last_row_col1, last_row_col2)
            data_frame = sheet.range('A1').expand().options(pd.DataFrame, header=1, index=False).value
            stock_exchange = sheet.range(f'A2:B{row}').options(dict).value
            watchlist = data_frame['Script Name'].to_list()

            # If watchlist has changed, update the feed
            if watchlist != previous_watchlist:
                print("Watchlist changed. Reconnecting the feed...")

                # Create new instruments and row mappings before disconnecting
                new_instruments, new_rows = create_instruments(watchlist, stock_exchange)

                # Disconnect the current connection
                data.disconnect()
                print("Disconnected from WebSocket feed.")

                # Update previous watchlist and rows before reconnecting
                previous_watchlist = watchlist
                rows = new_rows
                old_instruments = new_instruments

                # Reconnect with the updated instruments
                data = marketfeed.DhanFeed(client_id, access_token, new_instruments)
                data.run_forever()

            # Start receiving data
            response = data.get_data()

            if response:
                print(f"{datetime.datetime.now().time()}: LTP Received")
                if 'LTP' in response.keys():
                    df = pd.DataFrame(response, index=[0])
                    security_id = response['security_id']
                    row = rows.get(int(security_id), None)

                    if row:
                        df = df[['LTP', 'avg_price', 'volume', 'total_sell_quantity', 'open', 'close', 'high', 'low']]
                        sheet.range(f'C{row}').value = df.values.tolist()

    except Exception as e:
        print(f"WebSocket connection error: {e}")
        print("Reconnecting Again...")
        # time.sleep(5)  # Short delay before reconnecting
        run_feed(client_id, access_token, instruments)  # Retry the connection

def main_loop():
    # Fetch initial instrument data and start the feed
    last_row_col1 = sheet.range('A1').end('down').row
    last_row_col2 = sheet.range('B1').end('down').row
    row = max(last_row_col1, last_row_col2)
    data_frame = sheet.range('A1').expand().options(pd.DataFrame, header=1, index=False).value
    stock_exchange = sheet.range(f'A2:B{row}').options(dict).value
    watchlist = data_frame['Script Name'].to_list()

    instruments, rows = create_instruments(watchlist, stock_exchange)
    run_feed(client_id, access_token, instruments)

if __name__ == "__main__":
    main_loop()

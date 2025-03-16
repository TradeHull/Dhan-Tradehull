from dhanhq import dhanhq
import mibian
import datetime
import numpy as np
import pandas as pd
import traceback
import xlwings as xw
import requests
import pdb
import os
import time
import json
from json import loads as json_loads, dumps as json_dumps
from pprint import pprint
import logging
import warnings
from typing import Tuple, Dict

warnings.filterwarnings("ignore", category=FutureWarning)
print("Codebase Version 2.1")

class Tradehull:    
	clientCode                                      : str
	interval_parameters                             : dict
	instrument_file                                 : pd.core.frame.DataFrame
	step_df                                         : pd.core.frame.DataFrame
	index_step_dict                                 : dict
	index_underlying                                : dict
	call                                            : str
	put                                             : str

	def __init__(self,ClientCode:str,token_id:str):
		'''
		Clientcode                              = The ClientCode in string 
		token_id                                = The token_id in string 
		'''
		date_str = str(datetime.datetime.now().today().date())
		if not os.path.exists('Dependencies/log_files'):
			os.makedirs('Dependencies/log_files')
		file = 'Dependencies/log_files/logs' + date_str + '.log'
		logging.basicConfig(filename=file, level=logging.DEBUG,format='%(levelname)s:%(asctime)s:%(threadName)-10s:%(message)s') 
		self.logger = logging.getLogger()
		logging.info('Dhan.py  started system')
		logging.getLogger("requests").setLevel(logging.WARNING)
		logging.getLogger("urllib3").setLevel(logging.WARNING)
		self.logger.info("STARTED THE PROGRAM")

		try:
			self.status 							= dict()
			self.token_and_exchange 				= dict()
			self.get_login(ClientCode,token_id)
			self.token_and_exchange 				= {}
			self.interval_parameters                = {'minute':  60,'2minute':  120,'3minute':  180,'4minute':  240,'5minute':  300,'day':  86400,'10minute':  600,'15minute':  900,'30minute':  1800,'60minute':  3600,'day':86400}
			self.index_underlying                   = {"NIFTY 50":"NIFTY","NIFTY BANK":"BANKNIFTY","NIFTY FIN SERVICE":"FINNIFTY","NIFTY MID SELECT":"MIDCPNIFTY"}
			self.segment_dict                       = {"NSECM": 1, "NSEFO": 2, "NSECD": 3, "BSECM": 11, "BSEFO": 12, "MCXFO": 51}
			self.index_step_dict                    = {'MIDCPNIFTY':25,'SENSEX':100,'BANKEX':100,'NIFTY': 50, 'NIFTY 50': 50, 'NIFTY BANK': 100, 'BANKNIFTY': 100, 'NIFTY FIN SERVICE': 50, 'FINNIFTY': 50}
			self.token_dict 						= {'NIFTY':{'token':26000,'exchange':'NSECM'},'NIFTY 50':{'token':26000,'exchange':'NSECM'},'BANKNIFTY':{'token':26001,'exchange':'NSECM'},'NIFTY BANK':{'token':26001,'exchange':'NSECM'},'FINNIFTY':{'token':26034,'exchange':'NSECM'},'NIFTY FIN SERVICE':{'token':26034,'exchange':'NSECM'},'MIDCPNIFTY':{'token':26121,'exchange':'NSECM'},'NIFTY MID SELECT':{'token':26121,'exchange':'NSECM'},'SENSEX':{'token':26065,'exchange':'BSECM'},'BANKEX':{'token':26118,'exchange':'BSECM'}}
			self.intervals_dict 					= {'minute': 3, '2minute':4, '3minute': 4, '5minute': 5, '10minute': 10,'15minute': 15, '30minute': 25, '60minute': 40, 'day': 80}
			# self.stock_step_df						= {'NIFTY': 50, 'NIFTY 50': 50, 'NIFTY BANK': 100, 'BANKNIFTY': 100, 'NIFTY FIN SERVICE': 50, 'FINNIFTY': 50, 'AARTIIND': 5, 'ABB': 50, 'ABBOTINDIA': 250, 'ACC': 20, 'ADANIENT': 50, 'ADANIPORTS': 10, 'ALKEM': 20, 'AMBUJACEM': 10, 'APOLLOHOSP': 50, 'APOLLOTYRE': 5, 'ASHOKLEY': 1, 'ASIANPAINT': 20, 'ASTRAL': 20, 'ATUL': 50, 'AUBANK': 10, 'AUROPHARMA': 10, 'AXISBANK': 10, 'BAJAJ-AUTO': 50, 'BAJAJFINSV': 20, 'BAJFINANCE': 50, 'BALKRISIND': 20, 'BALRAMCHIN': 5, 'BATAINDIA': 10, 'BEL': 1, 'BERGEPAINT': 5, 'BHARATFORG': 10, 'BHARTIARTL': 10, 'BHEL': 1, 'BOSCHLTD': 100, 'BPCL': 5, 'BRITANNIA': 50, 'BSOFT': 10, 'CANBK': 5, 'CANFINHOME': 10, 'CHOLAFIN': 10, 'CIPLA': 10, 'COFORGE': 100, 'COLPAL': 10, 'CONCOR': 10, 'COROMANDEL': 10, 'CUB': 1, 'CUMMINSIND': 20, 'DABUR': 5, 'DALBHARAT': 20, 'DEEPAKNTR': 20, 'DELTACORP': 5, 'DIVISLAB': 50, 'DIXON': 50, 'DLF': 5, 'DRREDDY': 50, 'EICHERMOT': 50, 'ESCORTS': 20, 'FEDERALBNK': 1, 'GAIL': 1, 'GLENMARK': 10, 'GMRINFRA': 1, 'GNFC': 10, 'GODREJCP': 10, 'GODREJPROP': 20, 'GRASIM': 20, 'GUJGASLTD': 5, 'HAL': 20, 'HAVELLS': 10, 'HCLTECH': 10, 'HDFCAMC': 20, 'HDFCBANK': 10, 'HDFCLIFE': 5, 'HEROMOTOCO': 20, 'HINDALCO': 5, 'HINDCOPPER': 2.5, 'HINDUNILVR': 20, 'ICICIBANK': 10, 'ICICIGI': 10, 'ICICIPRULI': 5, 'IDEA': 1, 'IDFC': 1, 'IDFCFIRSTB': 1, 'IEX': 1, 'IGL': 5, 'INDHOTEL': 5, 'INDIAMART': 50, 'INDIGO': 20, 'INDUSINDBK': 20, 'INFY': 10, 'IOC': 1, 'IPCALAB': 10, 'IRCTC': 10, 'ITC': 5, 'JINDALSTEL': 10, 'JKCEMENT': 50, 'JSWSTEEL': 10, 'JUBLFOOD': 5, 'KOTAKBANK': 20, 'L&TFH': 1, 'LALPATHLAB': 20, 'LAURUSLABS': 5, 'LICHSGFIN': 5, 'LT': 20, 'LTIM': 50, 'LTTS': 50, 'LUPIN': 10, 'M&M': 10, 'M&MFIN': 5, 'MARICO': 5, 'MARUTI': 100, 'MCDOWELL-N': 10, 'MCX': 20, 'METROPOLIS': 20, 'MFSL': 10, 'MGL': 10, 'MOTHERSON': 1, 'MPHASIS': 20, 'MRF': 500, 'MUTHOOTFIN': 10, 'NATIONALUM': 1, 'NAUKRI': 50, 'NAVINFLUOR': 50, 'NESTLEIND': 100, 'NMDC': 1, 'NTPC': 1, 'OBEROIRLTY': 10, 'OFSS': 20, 'ONGC': 2.5, 'PAGEIND': 500, 'PEL': 10, 'PERSISTENT': 50, 'PIDILITIND': 20, 'PIIND': 50, 'PNB': 1, 'POLYCAB': 50, 'PVRINOX': 20, 'RAMCOCEM': 10, 'RELIANCE': 20, 'SAIL': 1, 'SBICARD': 10, 'SBILIFE': 10, 'SBIN': 5, 'SHREECEM': 250, 'SHRIRAMFIN': 20, 'SIEMENS': 50, 'SRF': 20, 'SUNPHARMA': 10, 'SUNTV': 5, 'SYNGENE': 10, 'TATACHEM': 10, 'TATACOMM': 20, 'TATACONSUM': 5, 'TATAMOTORS': 5, 'TATASTEEL': 1, 'TCS': 20, 'TECHM': 10, 'TITAN': 20, 'TORNTPHARM': 20, 'TRENT': 20, 'TVSMOTOR': 20, 'UBL': 10, 'ULTRACEMCO': 50, 'UPL': 5, 'VOLTAS': 10, 'ZYDUSLIFE': 5, 'ABCAPITAL': 2.5, 'ABFRL': 2.5, 'BANDHANBNK': 2.5, 'BANKBARODA': 2.5, 'BIOCON': 2.5, 'CHAMBLFERT': 5, 'COALINDIA': 2.5, 'CROMPTON': 2.5, 'EXIDEIND': 2.5, 'GRANULES': 2.5, 'HINDPETRO': 5, 'IBULHSGFIN': 2.5, 'INDIACEM': 2.5, 'INDUSTOWER': 2.5, 'MANAPPURAM': 2.5, 'PETRONET': 2.5, 'PFC': 2.5, 'POWERGRID': 2.5, 'RBLBANK': 2.5, 'RECLTD': 2.5, 'TATAPOWER': 5, 'VEDL': 2.5, 'WIPRO': 2.5, 'ZEEL': 2.5, 'AMARAJABAT': 10, 'APLLTD': 10, 'CADILAHC': 5, 'HDFC': 50, 'LTI': 100, 'MINDTREE': 20, 'MOTHERSUMI': 5, 'NAM-INDIA': 5, 'PFIZER': 50, 'PVR': 20, 'SRTRANSFIN': 20, 'TORNTPOWER': 5}
			self.stock_step_df                      = {'NIFTY': 50, 'BANKNIFTY': 100,'FINNIFTY': 50, 'AARTIIND': 5, 'ABB': 50, 'ABBOTINDIA': 250, 'ACC': 20, 'ADANIENT': 50, 'ADANIPORTS': 10, 'ALKEM': 20, 'AMBUJACEM': 10, 'APOLLOHOSP': 50, 'APOLLOTYRE': 5, 'ASHOKLEY': 1, 'ASIANPAINT': 20, 'ASTRAL': 20, 'ATUL': 50, 'AUBANK': 10, 'AUROPHARMA': 10, 'AXISBANK': 10, 'BAJAJ-AUTO': 50, 'BAJAJFINSV': 20, 'BAJFINANCE': 50, 'BALKRISIND': 20, 'BALRAMCHIN': 5, 'BATAINDIA': 10, 'BEL': 1, 'BERGEPAINT': 5, 'BHARATFORG': 10, 'BHARTIARTL': 10, 'BHEL': 1, 'BOSCHLTD': 100, 'BPCL': 5, 'BRITANNIA': 50, 'BSOFT': 10, 'CANBK': 5, 'CANFINHOME': 10, 'CHOLAFIN': 10, 'CIPLA': 10, 'COFORGE': 100, 'COLPAL': 10, 'CONCOR': 10, 'COROMANDEL': 10, 'CUB': 1, 'CUMMINSIND': 20, 'DABUR': 5, 'DALBHARAT': 20, 'DEEPAKNTR': 20, 'DELTACORP': 5, 'DIVISLAB': 50, 'DIXON': 50, 'DLF': 5, 'DRREDDY': 50, 'EICHERMOT': 50, 'ESCORTS': 20, 'FEDERALBNK': 1, 'GAIL': 1, 'GLENMARK': 10, 'GMRINFRA': 1, 'GNFC': 10, 'GODREJCP': 10, 'GODREJPROP': 20, 'GRASIM': 20, 'GUJGASLTD': 5, 'HAL': 20, 'HAVELLS': 10, 'HCLTECH': 10, 'HDFCAMC': 20, 'HDFCBANK': 10, 'HDFCLIFE': 5, 'HEROMOTOCO': 20, 'HINDALCO': 5, 'HINDCOPPER': 2.5, 'HINDUNILVR': 20, 'ICICIBANK': 10, 'ICICIGI': 10, 'ICICIPRULI': 5, 'IDEA': 1, 'IDFC': 1, 'IDFCFIRSTB': 1, 'IEX': 1, 'IGL': 5, 'INDHOTEL': 5, 'INDIAMART': 50, 'INDIGO': 20, 'INDUSINDBK': 20, 'INFY': 10, 'IOC': 1, 'IPCALAB': 10, 'IRCTC': 10, 'ITC': 5, 'JINDALSTEL': 10, 'JKCEMENT': 50, 'JSWSTEEL': 10, 'JUBLFOOD': 5, 'KOTAKBANK': 20, 'L&TFH': 1, 'LALPATHLAB': 20, 'LAURUSLABS': 5, 'LICHSGFIN': 5, 'LT': 20, 'LTIM': 50, 'LTTS': 50, 'LUPIN': 10, 'M&M': 10, 'M&MFIN': 5, 'MARICO': 5, 'MARUTI': 100, 'MCDOWELL-N': 10, 'MCX': 20, 'METROPOLIS': 20, 'MFSL': 10, 'MGL': 10, 'MOTHERSON': 1, 'MPHASIS': 20, 'MRF': 500, 'MUTHOOTFIN': 10, 'NATIONALUM': 1, 'NAUKRI': 50, 'NAVINFLUOR': 50, 'NESTLEIND': 100, 'NMDC': 1, 'NTPC': 1, 'OBEROIRLTY': 10, 'OFSS': 20, 'ONGC': 2.5, 'PAGEIND': 500, 'PEL': 10, 'PERSISTENT': 50, 'PIDILITIND': 20, 'PIIND': 50, 'PNB': 1, 'POLYCAB': 50, 'PVRINOX': 20, 'RAMCOCEM': 10, 'RELIANCE': 20, 'SAIL': 1, 'SBICARD': 10, 'SBILIFE': 10, 'SBIN': 5, 'SHREECEM': 250, 'SHRIRAMFIN': 20, 'SIEMENS': 50, 'SRF': 20, 'SUNPHARMA': 10, 'SUNTV': 5, 'SYNGENE': 10, 'TATACHEM': 10, 'TATACOMM': 20, 'TATACONSUM': 5, 'TATAMOTORS': 5, 'TATASTEEL': 1, 'TCS': 20, 'TECHM': 10, 'TITAN': 20, 'TORNTPHARM': 20, 'TRENT': 20, 'TVSMOTOR': 20, 'UBL': 10, 'ULTRACEMCO': 50, 'UPL': 5, 'VOLTAS': 10, 'ZYDUSLIFE': 5, 'ABCAPITAL': 2.5, 'ABFRL': 2.5, 'BANDHANBNK': 2.5, 'BANKBARODA': 2.5, 'BIOCON': 2.5, 'CHAMBLFERT': 5, 'COALINDIA': 2.5, 'CROMPTON': 2.5, 'EXIDEIND': 2.5, 'GRANULES': 2.5, 'HINDPETRO': 5, 'IBULHSGFIN': 2.5, 'INDIACEM': 2.5, 'INDUSTOWER': 2.5, 'MANAPPURAM': 2.5, 'PETRONET': 2.5, 'PFC': 2.5, 'POWERGRID': 2.5, 'RBLBANK': 2.5, 'RECLTD': 2.5, 'TATAPOWER': 5, 'VEDL': 2.5, 'WIPRO': 2.5, 'ZEEL': 2.5, 'AMARAJABAT': 10, 'APLLTD': 10, 'CADILAHC': 5, 'HDFC': 50, 'LTI': 100, 'MINDTREE': 20, 'MOTHERSUMI': 5, 'NAM-INDIA': 5, 'PFIZER': 50, 'PVR': 20, 'SRTRANSFIN': 20, 'TORNTPOWER': 5}
			self.commodity_step_dict 				= {'GOLD': 100,'SILVER': 100,'CRUDEOIL': 50,'NATURALGAS': 10,'COPPER': 5,'NICKEL': 10,'ZINC': 2.5,'LEAD': 1,         'ALUMINIUM': 1,    'COTTON': 100,     'MENTHAOIL': 10,   'GOLDM': 50,       'GOLDPETAL': 5,    'GOLDGUINEA': 10,  'SILVERM': 50,     'SILVERMIC': 10,   'BRASS': 5,        'CASTORSEED': 100, 'COTTONSEEDOILCAKE''CARDAMOM': 50,    'RBDPALMOLEIN': 10,'CRUDEPALMOIL': 10,'PEPPER': 100,     'JEERA': 100,      'SOYABEAN': 50,    'SOYAOIL': 10,     'TURMERIC': 100,   'GUARGUM': 100,    'GUARSEED': 100,   'CHANA': 50,       'MUSTARDSEED': 50, 'BARLEY': 50,      'SUGARM': 50,      'WHEAT': 50,       'MAIZE': 50,       'PADDY': 50,       'BAJRA': 50,       'JUTE': 50,        'RUBBER': 100,     'COFFEE': 50,      'COPRA': 50,       'SESAMESEED': 50,  'TEA': 100,        'KAPAS': 100,      'BARLEYFEED': 50,  'RAPESEED': 50,    'LINSEED': 50,     'SUNFLOWER': 50,   'CORIANDER': 50,   'CUMINSEED': 100   }
			self.start_date, self.end_date          = self.get_start_date()
			try:
				self.step_df                        = pd.read_excel("https://archives.nseindia.com/content/fo/sos_scheme.xls")
			except Exception as e:
				print("step Value DF is not generated due to Error from NSE India site: ", e)
				print("Collecting step values from program memory.")
				step_value_dict                    = {'NIFTY': 50, 'NIFTY 50': 50, 'NIFTY BANK': 100, 'BANKNIFTY': 100, 'NIFTY FIN SERVICE': 50, 'FINNIFTY': 50, 'AARTIIND': 5, 'ABB': 50, 'ABBOTINDIA': 250, 'ACC': 20, 'ADANIENT': 50, 'ADANIPORTS': 10, 'ALKEM': 20, 'AMBUJACEM': 10, 'APOLLOHOSP': 50, 'APOLLOTYRE': 5, 'ASHOKLEY': 1, 'ASIANPAINT': 20, 'ASTRAL': 20, 'ATUL': 50, 'AUBANK': 10, 'AUROPHARMA': 10, 'AXISBANK': 10, 'BAJAJ-AUTO': 50, 'BAJAJFINSV': 20, 'BAJFINANCE': 50, 'BALKRISIND': 20, 'BALRAMCHIN': 5, 'BATAINDIA': 10, 'BEL': 1, 'BERGEPAINT': 5, 'BHARATFORG': 10, 'BHARTIARTL': 10, 'BHEL': 1, 'BOSCHLTD': 100, 'BPCL': 5, 'BRITANNIA': 50, 'BSOFT': 10, 'CANBK': 5, 'CANFINHOME': 10, 'CHOLAFIN': 10, 'CIPLA': 10, 'COFORGE': 100, 'COLPAL': 10, 'CONCOR': 10, 'COROMANDEL': 10, 'CUB': 1, 'CUMMINSIND': 20, 'DABUR': 5, 'DALBHARAT': 20, 'DEEPAKNTR': 20, 'DELTACORP': 5, 'DIVISLAB': 50, 'DIXON': 50, 'DLF': 5, 'DRREDDY': 50, 'EICHERMOT': 50, 'ESCORTS': 20, 'FEDERALBNK': 1, 'GAIL': 1, 'GLENMARK': 10, 'GMRINFRA': 1, 'GNFC': 10, 'GODREJCP': 10, 'GODREJPROP': 20, 'GRASIM': 20, 'GUJGASLTD': 5, 'HAL': 20, 'HAVELLS': 10, 'HCLTECH': 10, 'HDFCAMC': 20, 'HDFCBANK': 10, 'HDFCLIFE': 5, 'HEROMOTOCO': 20, 'HINDALCO': 5, 'HINDCOPPER': 2.5, 'HINDUNILVR': 20, 'ICICIBANK': 10, 'ICICIGI': 10, 'ICICIPRULI': 5, 'IDEA': 1, 'IDFC': 1, 'IDFCFIRSTB': 1, 'IEX': 1, 'IGL': 5, 'INDHOTEL': 5, 'INDIAMART': 50, 'INDIGO': 20, 'INDUSINDBK': 20, 'INFY': 10, 'IOC': 1, 'IPCALAB': 10, 'IRCTC': 10, 'ITC': 5, 'JINDALSTEL': 10, 'JKCEMENT': 50, 'JSWSTEEL': 10, 'JUBLFOOD': 5, 'KOTAKBANK': 20, 'L&TFH': 1, 'LALPATHLAB': 20, 'LAURUSLABS': 5, 'LICHSGFIN': 5, 'LT': 20, 'LTIM': 50, 'LTTS': 50, 'LUPIN': 10, 'M&M': 10, 'M&MFIN': 5, 'MARICO': 5, 'MARUTI': 100, 'MCDOWELL-N': 10, 'MCX': 20, 'METROPOLIS': 20, 'MFSL': 10, 'MGL': 10, 'MOTHERSON': 1, 'MPHASIS': 20, 'MRF': 500, 'MUTHOOTFIN': 10, 'NATIONALUM': 1, 'NAUKRI': 50, 'NAVINFLUOR': 50, 'NESTLEIND': 100, 'NMDC': 1, 'NTPC': 1, 'OBEROIRLTY': 10, 'OFSS': 20, 'ONGC': 2.5, 'PAGEIND': 500, 'PEL': 10, 'PERSISTENT': 50, 'PIDILITIND': 20, 'PIIND': 50, 'PNB': 1, 'POLYCAB': 50, 'PVRINOX': 20, 'RAMCOCEM': 10, 'RELIANCE': 20, 'SAIL': 1, 'SBICARD': 10, 'SBILIFE': 10, 'SBIN': 5, 'SHREECEM': 250, 'SHRIRAMFIN': 20, 'SIEMENS': 50, 'SRF': 20, 'SUNPHARMA': 10, 'SUNTV': 5, 'SYNGENE': 10, 'TATACHEM': 10, 'TATACOMM': 20, 'TATACONSUM': 5, 'TATAMOTORS': 5, 'TATASTEEL': 1, 'TCS': 20, 'TECHM': 10, 'TITAN': 20, 'TORNTPHARM': 20, 'TRENT': 20, 'TVSMOTOR': 20, 'UBL': 10, 'ULTRACEMCO': 50, 'UPL': 5, 'VOLTAS': 10, 'ZYDUSLIFE': 5, 'ABCAPITAL': 2.5, 'ABFRL': 2.5, 'BANDHANBNK': 2.5, 'BANKBARODA': 2.5, 'BIOCON': 2.5, 'CHAMBLFERT': 5, 'COALINDIA': 2.5, 'CROMPTON': 2.5, 'EXIDEIND': 2.5, 'GRANULES': 2.5, 'HINDPETRO': 5, 'IBULHSGFIN': 2.5, 'INDIACEM': 2.5, 'INDUSTOWER': 2.5, 'MANAPPURAM': 2.5, 'PETRONET': 2.5, 'PFC': 2.5, 'POWERGRID': 2.5, 'RBLBANK': 2.5, 'RECLTD': 2.5, 'TATAPOWER': 5, 'VEDL': 2.5, 'WIPRO': 2.5, 'ZEEL': 2.5, 'AMARAJABAT': 10, 'APLLTD': 10, 'CADILAHC': 5, 'HDFC': 50, 'LTI': 100, 'MINDTREE': 20, 'MOTHERSUMI': 5, 'NAM-INDIA': 5, 'PFIZER': 50, 'PVR': 20, 'SRTRANSFIN': 20, 'TORNTPOWER': 5}
				self.step_df                        = pd.DataFrame.from_dict(step_value_dict, orient='index')
				self.step_df                        = self.step_df.reset_index()
				self.step_df.rename({"index": "Symbol", 0: "Applicable Step value"}, axis='columns', inplace =True)
		except Exception as e:
			print(e)
			traceback.print_exc()

	def get_login(self,ClientCode,token_id):
		try:
			self.ClientCode 									= ClientCode
			self.token_id										= token_id
			print("-----Logged into Dhan-----")
			self.Dhan = dhanhq(self.ClientCode, self.token_id)
			self.instrument_df 									= self.get_instrument_file()
			print('Got the instrument file')
		except Exception as e:
			print(e)
			self.logger.exception(f'got exception in get_login as {e} ')
			print(self.response)
			traceback.print_exc()

	def get_instrument_file(self):
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
				print(f"reading existing file {expected_file}")
				instrument_df = pd.read_csv("Dependencies\\" + expected_file, low_memory=False)
			except Exception as e:
				print(
					"This BOT Is Instrument file is not generated completely, Picking New File from Dhan Again")
				instrument_df = pd.read_csv("https://images.dhan.co/api-data/api-scrip-master.csv", low_memory=False)
				instrument_df.to_csv("Dependencies\\" + expected_file)
		else:
			# this will fetch instrument_df file from Dhan
			print("This BOT Is Picking New File From Dhan")
			instrument_df = pd.read_csv("https://images.dhan.co/api-data/api-scrip-master.csv", low_memory=False)
			instrument_df.to_csv("Dependencies\\" + expected_file)
		return instrument_df

	def order_placement(self,tradingsymbol:str, exchange:str,quantity:int, price:int, trigger_price:int, order_type:str, transaction_type:str, trade_type:str)->str:
		try:
			# script_exchange = {"NSE":self.Dhan.NSE, "NFO":self.Dhan.NSE_FNO, "BFO":self.Dhan.BSE_FNO, "CUR": self.Dhan.CUR, "BSE":self.Dhan.BSE, "MCX":self.Dhan.MCX}
			script_exchange = {"NSE":self.Dhan.NSE, "NFO":self.Dhan.FNO, "BFO":self.Dhan.FNO, "CUR": self.Dhan.CUR, "BSE":self.Dhan.BSE, "MCX":self.Dhan.MCX}
			self.order_Type = {'LIMIT': self.Dhan.LIMIT, 'MARKET': self.Dhan.MARKET,'STOPLIMIT': self.Dhan.SL, 'STOPMARKET': self.Dhan.SLM}
			product = {'MIS':self.Dhan.INTRA, 'MARGIN':self.Dhan.MARGIN, 'MTF':self.Dhan.MTF, 'CO':self.Dhan.CO,'BO':self.Dhan.BO, 'CNC': self.Dhan.CNC}
			Validity = {'DAY': "DAY", 'IOC': 'IOC'}
			transactiontype = {'BUY': self.Dhan.BUY, 'SELL': self.Dhan.SELL}
			instrument_exchange = {'NSE':"NSE",'BSE':"BSE",'NFO':'NSE','BFO':'BSE','MCX':'MCX','CUR':'NSE'}

			exchangeSegment = script_exchange[exchange]
			product_Type = product[trade_type.upper()]
			order_type = self.order_Type[order_type.upper()]
			order_side = transactiontype[transaction_type.upper()]
			time_in_force = Validity['DAY']
			security_id = self.instrument_df[((self.instrument_df['SEM_TRADING_SYMBOL']==tradingsymbol)|(self.instrument_df['SEM_CUSTOM_SYMBOL']==tradingsymbol))&(self.instrument_df['SEM_EXM_EXCH_ID']==instrument_exchange[exchange])].iloc[-1]['SEM_SMST_SECURITY_ID']

			order = self.Dhan.place_order(security_id=str(security_id), exchange_segment=exchangeSegment,
											   transaction_type=order_side, quantity=quantity,
											   order_type=order_type, product_type=product_Type, price=price,
											   trigger_price=trigger_price)

			orderid = order["data"]["orderId"]
			return str(orderid)
		except Exception as e:
			self.logger.exception(f'Got exception in place_order as {e}')
			traceback.print_exc()
			return None

	def kill_switch(self,action):
		try:
			active = {'ON':'ACTIVATE','OFF':'DEACTIVATE'}
			current_action = active[action.upper()]

			killswitch_response = self.Dhan.kill_switch(current_action)	
			if 'killSwitchStatus' in killswitch_response['data'].keys():
				return killswitch_response['data']['killSwitchStatus']
			else:
				return killswitch_response
		except Exception as e:
			self.logger.exception(f"Error at Kill switch as {e}")


	def get_live_pnl(self):
		"""
			use to get live pnl
			pnl()
		"""
		try:
			instrument_df = self.instrument_df.copy()
			time.sleep(1)
			pos_book = self.Dhan.get_positions()
			if pos_book['status']=='failure':
				raise Exception(pos_book)
			pos_book_dict = pos_book['data']
			pos_book = pd.DataFrame(pos_book_dict)
			live_pnl = []
			ltp_list = list()

			if pos_book.empty:
				return 0
			for pos_ in pos_book_dict:
				security_id = int(pos_['securityId'])
				underlying = instrument_df[((instrument_df['SEM_SMST_SECURITY_ID']==security_id))].iloc[-1]['SEM_CUSTOM_SYMBOL']
				ltp_list.append(underlying)

			ltp_data = self.get_ltp_data(ltp_list)

			for pos_ in pos_book_dict:
				security_id = int(pos_['securityId'])
				underlying = instrument_df[((instrument_df['SEM_SMST_SECURITY_ID']==security_id))].iloc[-1]['SEM_CUSTOM_SYMBOL']
				# closePrice = self.get_ltp(underlying)
				closePrice = ltp_data[underlying]
				Total_MTM = (float(pos_['daySellValue']) - float(pos_['dayBuyValue'])) + (int(pos_['netQty']) *closePrice * float(pos_['multiplier']))
				live_pnl.append(Total_MTM)
			
			return sum(live_pnl)
		except Exception as e:
			print(f"got exception in pnl as {e}")
			self.logger.exception(f'got exception in pnl as {e} ')
			return 0

	def get_balance(self):
		try:
			response = self.Dhan.get_fund_limits()
			if response['status']!='failure':
				balance = float(response['data']['availabelBalance'])
				return balance
			else:
				raise Exception(response)
		except Exception as e:
			print(f"Error at Gettting balance as {e}")
			self.logger.exception(f"Error at Gettting balance as {e}")
			return 0
	

	def convert_to_date_time(self,time):
		return self.Dhan.convert_to_date_time(time)
	

	def get_start_date(self):
		try:
			instrument_df = self.instrument_df.copy()
			from_date= datetime.datetime.now()-datetime.timedelta(days=100)
			start_date = (datetime.datetime.now()-datetime.timedelta(days=5)).strftime('%Y-%m-%d')
			from_date = from_date.strftime('%Y-%m-%d')
			to_date = datetime.datetime.now().strftime('%Y-%m-%d')
			instrument_exchange = {'NSE':"NSE",'BSE':"BSE",'NFO':'NSE','BFO':'BSE','MCX':'MCX','CUR':'NSE'}
			tradingsymbol = "NIFTY"
			exchange = "NSE"
			exchange_segment = self.Dhan.INDEX
			security_id 	= instrument_df[((instrument_df['SEM_TRADING_SYMBOL']==tradingsymbol)|(instrument_df['SEM_CUSTOM_SYMBOL']==tradingsymbol))&(instrument_df['SEM_EXM_EXCH_ID']==instrument_exchange[exchange])].iloc[-1]['SEM_SMST_SECURITY_ID']
			instrument_type = instrument_df[((instrument_df['SEM_TRADING_SYMBOL']==tradingsymbol)|(instrument_df['SEM_CUSTOM_SYMBOL']==tradingsymbol))&(instrument_df['SEM_EXM_EXCH_ID']==instrument_exchange[exchange])].iloc[-1]['SEM_INSTRUMENT_NAME']
			expiry_code 	= instrument_df[((instrument_df['SEM_TRADING_SYMBOL']==tradingsymbol)|(instrument_df['SEM_CUSTOM_SYMBOL']==tradingsymbol))&(instrument_df['SEM_EXM_EXCH_ID']==instrument_exchange[exchange])].iloc[-1]['SEM_EXPIRY_CODE']
			ohlc = self.Dhan.historical_daily_data(int(security_id),exchange_segment,instrument_type,from_date,to_date,int(expiry_code))
			if ohlc['status']!='failure':
				df = pd.DataFrame(ohlc['data'])
				if not df.empty:
					df['timestamp'] = df['timestamp'].apply(lambda x: self.convert_to_date_time(x))
					start_date = df.iloc[-2]['timestamp']
					start_date = start_date.strftime('%Y-%m-%d')
					return start_date, to_date
				else:
					return start_date, to_date
			else:
				return start_date, to_date			
		except Exception as e:
			self.logger.exception(f"Error at getting start date as {e}")
			return start_date, to_date

	def get_historical_data(self,tradingsymbol,exchange,timeframe, debug="NO"):			
		try:
			instrument_df = self.instrument_df.copy()
			from_date= datetime.datetime.now()-datetime.timedelta(days=365)
			from_date = from_date.strftime('%Y-%m-%d')
			to_date = datetime.datetime.now().strftime('%Y-%m-%d') 
			# script_exchange = {"NSE":self.Dhan.NSE, "NFO":self.Dhan.NSE_FNO, "BFO":self.Dhan.BSE_FNO, "CUR": self.Dhan.CUR, "BSE":self.Dhan.BSE, "MCX":self.Dhan.MCX}
			script_exchange = {"NSE":self.Dhan.NSE, "NFO":self.Dhan.FNO, "BFO":self.Dhan.FNO, "CUR": self.Dhan.CUR, "BSE":self.Dhan.BSE, "MCX":self.Dhan.MCX, "INDEX":self.Dhan.INDEX}
			instrument_exchange = {'NSE':"NSE",'BSE':"BSE",'NFO':'NSE','BFO':'BSE','MCX':'MCX','CUR':'NSE'}
			exchange_segment = script_exchange[exchange]
			index_exchange = {"NIFTY":'NSE',"BANKNIFTY":"NSE","FINNIFTY":"NSE","MIDCPNIFTY":"NSE","BANKEX":"BSE","SENSEX":"BSE"}
			if tradingsymbol in index_exchange:
				exchange =index_exchange[tradingsymbol]		
			security_id 	= instrument_df[((instrument_df['SEM_TRADING_SYMBOL']==tradingsymbol)|(instrument_df['SEM_CUSTOM_SYMBOL']==tradingsymbol))&(instrument_df['SEM_EXM_EXCH_ID']==instrument_exchange[exchange])].iloc[-1]['SEM_SMST_SECURITY_ID']
			Symbol 			= instrument_df[((instrument_df['SEM_TRADING_SYMBOL']==tradingsymbol)|(instrument_df['SEM_CUSTOM_SYMBOL']==tradingsymbol))&(instrument_df['SEM_EXM_EXCH_ID']==instrument_exchange[exchange])].iloc[-1]['SEM_TRADING_SYMBOL']
			instrument_type = instrument_df[((instrument_df['SEM_TRADING_SYMBOL']==tradingsymbol)|(instrument_df['SEM_CUSTOM_SYMBOL']==tradingsymbol))&(instrument_df['SEM_EXM_EXCH_ID']==instrument_exchange[exchange])].iloc[-1]['SEM_INSTRUMENT_NAME']
			expiry_code 	= instrument_df[((instrument_df['SEM_TRADING_SYMBOL']==tradingsymbol)|(instrument_df['SEM_CUSTOM_SYMBOL']==tradingsymbol))&(instrument_df['SEM_EXM_EXCH_ID']==instrument_exchange[exchange])].iloc[-1]['SEM_EXPIRY_CODE']
			if timeframe in ['1', '5', '15', '25', '60']:
				interval = int(timeframe)
			elif timeframe=="DAY":
				pass
			else:
				raise Exception("interval value must be ['1','5','15','25','60','DAY']")
			if timeframe == "DAY":			
				ohlc = self.Dhan.historical_daily_data(int(security_id),exchange_segment,instrument_type,from_date,to_date,int(expiry_code))
			else:
				ohlc = self.Dhan.intraday_minute_data(str(security_id),exchange_segment,instrument_type,self.start_date,self.end_date,int(interval))
			
			if debug.upper()=="YES":
				print(ohlc)
			
			if ohlc['status']!='failure':
				df = pd.DataFrame(ohlc['data'])
				if not df.empty:
					df['timestamp'] = df['timestamp'].apply(lambda x: self.convert_to_date_time(x))
					return df
				else:
					return df
			else:
				raise Exception(ohlc) 
		except Exception as e:
			print(f"Exception in Getting OHLC data as {e}")
			self.logger.exception(f"Exception in Getting OHLC data as {e}")
			# traceback.print_exc()

	def get_intraday_data(self,tradingsymbol,exchange,timeframe, debug="NO"):			
		try:
			instrument_df = self.instrument_df.copy()
			available_frames = {
				2: '2T',    # 2 minutes
				3: '3T',    # 3 minutes
				5: '5T',    # 5 minutes
				10: '10T',   # 10 minutes
				15: '15T',   # 15 minutes
				30: '30T',   # 30 minutes
				60: '60T'    # 60 minutes
			}

			start_date =datetime.datetime.now().strftime('%Y-%m-%d')
			end_date = datetime.datetime.now().strftime('%Y-%m-%d')

			# script_exchange = {"NSE":self.Dhan.NSE, "NFO":self.Dhan.NSE_FNO, "BFO":self.Dhan.BSE_FNO, "CUR": self.Dhan.CUR, "BSE":self.Dhan.BSE, "MCX":self.Dhan.MCX}
			script_exchange = {"NSE":self.Dhan.NSE, "NFO":self.Dhan.FNO, "BFO":self.Dhan.FNO, "CUR": self.Dhan.CUR, "BSE":self.Dhan.BSE, "MCX":self.Dhan.MCX, "INDEX":self.Dhan.INDEX}
			instrument_exchange = {'NSE':"NSE",'BSE':"BSE",'NFO':'NSE','BFO':'BSE','MCX':'MCX','CUR':'NSE'}
			exchange_segment = script_exchange[exchange]
			index_exchange = {"NIFTY":'NSE',"BANKNIFTY":"NSE","FINNIFTY":"NSE","MIDCPNIFTY":"NSE","BANKEX":"BSE","SENSEX":"BSE"}
			if tradingsymbol in index_exchange:
				exchange =index_exchange[tradingsymbol]	
			security_id 	= instrument_df[((instrument_df['SEM_TRADING_SYMBOL']==tradingsymbol)|(instrument_df['SEM_CUSTOM_SYMBOL']==tradingsymbol))&(instrument_df['SEM_EXM_EXCH_ID']==instrument_exchange[exchange])].iloc[-1]['SEM_SMST_SECURITY_ID']
			instrument_type = instrument_df[((instrument_df['SEM_TRADING_SYMBOL']==tradingsymbol)|(instrument_df['SEM_CUSTOM_SYMBOL']==tradingsymbol))&(instrument_df['SEM_EXM_EXCH_ID']==instrument_exchange[exchange])].iloc[-1]['SEM_INSTRUMENT_NAME']
			ohlc = self.Dhan.intraday_minute_data(str(security_id),exchange_segment,instrument_type,start_date,end_date,int(1))
			
			if debug.upper()=="YES":
				print(ohlc)

			if ohlc['status']!='failure':
				df = pd.DataFrame(ohlc['data'])
				if not df.empty:
					df['timestamp'] = df['timestamp'].apply(lambda x: self.convert_to_date_time(x))
					if timeframe==1:
						return df
					df = self.resample_timeframe(df,available_frames[timeframe])
					return df
				else:
					return df
			else:
				raise Exception(ohlc) 
		except Exception as e:
			print(e)
			self.logger.exception(f"Exception in Getting OHLC data as {e}")
			traceback.print_exc()

	def resample_timeframe(self, df, timeframe='5T'):
		df['timestamp'] = pd.to_datetime(df['timestamp'])
		df.set_index('timestamp', inplace=True)
		earliest_time = df.index.min()
		desired_start_time = earliest_time.replace(hour=9, minute=15, second=0, microsecond=0)
		
		if earliest_time < desired_start_time:
			adjusted_start_time = desired_start_time
		else:
			adjusted_start_time = desired_start_time + pd.DateOffset(minutes=(earliest_time - desired_start_time).seconds // 60 // int(timeframe[:-1]) * int(timeframe[:-1]))
		
		resampled_df = df.resample(timeframe, origin=adjusted_start_time).agg({
			'open': 'first',
			'high': 'max',
			'low': 'min',
			'close': 'last',
			'volume': 'sum'
		})
		
		resampled_df.reset_index(inplace=True)
		
		return resampled_df

	
	def get_lot_size(self,tradingsymbol: str):
		instrument_df = self.instrument_df.copy()
		data = instrument_df[((instrument_df['SEM_TRADING_SYMBOL']==tradingsymbol)|(instrument_df['SEM_CUSTOM_SYMBOL']==tradingsymbol))]
		if len(data) == 0:
			self.logger.exception("Enter valid Script Name")
			return 0
		else:
			return int(data.iloc[0]['SEM_LOT_UNITS'])
		

	def get_ltp_data(self,names, debug="NO"):
		try:
			instrument_df = self.instrument_df.copy()
			instruments = {'NSE_EQ':[],'IDX_I':[],'NSE_FNO':[],'NSE_CURRENCY':[],'BSE_EQ':[],'BSE_FNO':[],'BSE_CURRENCY':[],'MCX_COMM':[]}
			instrument_names = {}
			NFO = ["BANKNIFTY","NIFTY","MIDCPNIFTY","FINNIFTY"]
			BFO = ['SENSEX','BANKEX']
			equity = ['CALL','PUT','FUT']			
			exchange_index = {"BANKNIFTY": "NSE_IDX","NIFTY":"NSE_IDX","MIDCPNIFTY":"NSE_IDX", "FINNIFTY":"NSE_IDX","SENSEX":"BSE_IDX","BANKEX":"BSE_IDX"}
			if not isinstance(names, list):
				names = [names]
			for name in names:
				try:
					if name in exchange_index.keys():
						security_id = instrument_df[((instrument_df['SEM_CUSTOM_SYMBOL']==name)|(instrument_df['SEM_TRADING_SYMBOL']==name))].iloc[-1]['SEM_SMST_SECURITY_ID']
						instruments['IDX_I'].append(int(security_id))
						instrument_names[str(security_id)]=name
					elif name in self.commodity_step_dict.keys():
						security_id = instrument_df[(instrument_df['SEM_EXM_EXCH_ID']=='MCX')&(instrument_df['SM_SYMBOL_NAME']==name.upper())&(instrument_df['SEM_INSTRUMENT_NAME']=='FUTCOM')].sort_values(by='SEM_EXPIRY_DATE').iloc[0]['SEM_SMST_SECURITY_ID']
						instruments['MCX_COMM'].append(int(security_id))
						instrument_names[str(security_id)]=name
					else:
						security_id = instrument_df[((instrument_df['SEM_CUSTOM_SYMBOL']==name)|(instrument_df['SEM_TRADING_SYMBOL']==name))].iloc[-1]['SEM_SMST_SECURITY_ID']
						nfo_check = ['NSE_FNO' for nfo in NFO if nfo in name]
						bfo_check = ['BSE_FNO' for bfo in BFO if bfo in name]
						exchange_nfo ='NSE_FNO' if len(nfo_check)!=0 else False
						exchange_bfo = 'BSE_FNO' if len(bfo_check)!=0 else False
						if not exchange_nfo and not exchange_bfo:
							eq_check =['NSE_FNO' for nfo in equity if nfo in name]
							exchange_eq ='NSE_FNO' if len(eq_check)!=0 else "NSE_EQ"
						else:
							exchange_eq="NSE_EQ"
						exchange ='NSE_FNO' if exchange_nfo else ('BSE_FNO' if exchange_bfo else exchange_eq)
						trail_exchange = exchange
						mcx_check = ['MCX_COMM' for mcx in self.commodity_step_dict.keys() if mcx in name]
						exchange = "MCX_COMM" if len(mcx_check)!=0 else exchange
						if exchange == "MCX_COMM": 
							if instrument_df[((instrument_df['SEM_CUSTOM_SYMBOL']==name)|(instrument_df['SEM_TRADING_SYMBOL']==name))&(instrument_df['SEM_EXM_EXCH_ID']=='MCX')].empty:
								exchange = trail_exchange
						if exchange == "MCX_COMM":
							security_id = instrument_df[((instrument_df['SEM_CUSTOM_SYMBOL']==name)|(instrument_df['SEM_TRADING_SYMBOL']==name))&(instrument_df['SEM_EXM_EXCH_ID']=='MCX')].iloc[-1]['SEM_SMST_SECURITY_ID']
						instruments[exchange].append(int(security_id))
						instrument_names[str(security_id)]=name
				except Exception as e:
					print(name)
					self.logger.error(f"Exception for instrument name {name} as {e}")
			time.sleep(0.7)
			data = self.Dhan.ticker_data(instruments)
			ltp_data=dict()
			
			if debug.upper()=="YES":
				print(data)			

			if data['status']!='failure':
				all_values = data['data']['data']
				for exchange in data['data']['data']:
					for key, values in all_values[exchange].items():
						symbol = instrument_names[key]
						ltp_data[symbol] = values['last_price']
			else:
				raise Exception(data)
			
			return ltp_data
		except Exception as e:
			print(f"Exception at calling ltp as {e}")
			self.logger.exception(f"Exception at calling ltp as {e}")
			return dict()

	
	def ltp_call(self,instruments):
		try:
			url = "https://api.dhan.co/v2/marketfeed/ltp"
			headers = {
				'Accept': 'application/json',
				'Content-Type': 'application/json',
				'access-token': self.token_id,
				'client-id': self.ClientCode
			}
			
			data = dict()
			for key, value in instruments.items():
				if len(value)!=0:
					data[key]=value
					data[key] = [int(val) if isinstance(val, np.integer) else float(val) if isinstance(val, np.floating) else val for val in value]
			# data = {'IDX_I': [13,],'MCX_COMM': [432293],"NSE_EQ":[11536],}

			response = requests.post(url, headers=headers, json=data)
			if response.status_code == 200:
				return response.json()
			else:
				raise Exception(f"Failed to retrieve LTP. Status Code: {response.status_code}, Response: {response.text}")		
		except Exception as e:
			self.logger.exception(f"Exception at getting ltp from api as {e}")



	def ATM_Strike_Selection(self, Underlying, Expiry):
		try:
			Expiry = pd.to_datetime(Expiry, format='%d-%m-%Y').strftime('%Y-%m-%d')
			exchange_index = {"BANKNIFTY": "NSE","NIFTY":"NSE","MIDCPNIFTY":"NSE", "FINNIFTY":"NSE","SENSEX":"BSE","BANKEX":"BSE"}
			instrument_df = self.instrument_df.copy()

			instrument_df['SEM_EXPIRY_DATE'] = pd.to_datetime(instrument_df['SEM_EXPIRY_DATE'], errors='coerce')
			instrument_df['ContractExpiration'] = instrument_df['SEM_EXPIRY_DATE'].dt.date
			instrument_df['ContractExpiration'] = instrument_df['ContractExpiration'].astype(str)

			if Underlying in exchange_index:
				exchange = exchange_index[Underlying]
			elif Underlying in self.commodity_step_dict.keys():
				exchange = "MCX"
			else:
				# exchange = instrument_df[((instrument_df['SEM_TRADING_SYMBOL']==Underlying)|(instrument_df['SEM_CUSTOM_SYMBOL']==Underlying))].iloc[0]['SEM_EXM_EXCH_ID']
				exchange = "NSE"
	
			ltp_data = self.get_ltp_data(Underlying)
			ltp = ltp_data[Underlying]
			if Underlying in self.index_step_dict:
				step = self.index_step_dict[Underlying]
			if Underlying in self.stock_step_df:
				step = self.stock_step_df[Underlying]
			if Underlying in self.commodity_step_dict:
				step = self.commodity_step_dict[Underlying]
			strike = round(ltp/step) * step
			
			if exchange !="MCX":
				ce_condition = (instrument_df['SEM_EXM_EXCH_ID'] == exchange) & ((instrument_df['SEM_TRADING_SYMBOL'].str.contains(Underlying))|(instrument_df['SEM_CUSTOM_SYMBOL'].str.contains(Underlying))) & (instrument_df['ContractExpiration'] == Expiry) & (instrument_df['SEM_OPTION_TYPE']=='CE') 
				pe_condition = (instrument_df['SEM_EXM_EXCH_ID'] == exchange) & ((instrument_df['SEM_TRADING_SYMBOL'].str.contains(Underlying))|(instrument_df['SEM_CUSTOM_SYMBOL'].str.contains(Underlying))) & (instrument_df['ContractExpiration'] == Expiry) & (instrument_df['SEM_OPTION_TYPE']=='PE')
			else: 		
				ce_condition = (instrument_df['SEM_EXM_EXCH_ID'] == exchange) & ((instrument_df['SEM_TRADING_SYMBOL'].str.contains(Underlying))|(instrument_df['SEM_CUSTOM_SYMBOL'].str.contains(Underlying))) & (instrument_df['ContractExpiration'] == Expiry) & (instrument_df['SEM_OPTION_TYPE']=='CE') & (instrument_df['SM_SYMBOL_NAME']==Underlying) 
				pe_condition = (instrument_df['SEM_EXM_EXCH_ID'] == exchange) & ((instrument_df['SEM_TRADING_SYMBOL'].str.contains(Underlying))|(instrument_df['SEM_CUSTOM_SYMBOL'].str.contains(Underlying))) & (instrument_df['ContractExpiration'] == Expiry) & (instrument_df['SEM_OPTION_TYPE']=='PE')	& (instrument_df['SM_SYMBOL_NAME']==Underlying)			
			ce_df = instrument_df[ce_condition].copy()
			pe_df = instrument_df[pe_condition].copy()

			ce_df['SEM_STRIKE_PRICE'] = ce_df['SEM_STRIKE_PRICE'].astype("int")
			pe_df['SEM_STRIKE_PRICE'] = pe_df['SEM_STRIKE_PRICE'].astype("int")

			ce_df =ce_df[ce_df['SEM_STRIKE_PRICE']==strike]
			pe_df =pe_df[pe_df['SEM_STRIKE_PRICE']==strike]

			if ce_df.empty or len(ce_df)==0:
				ce_df['diff'] = abs(ce_df['SEM_STRIKE_PRICE'] - strike)
				closest_index = ce_df['diff'].idxmin()
				strike = ce_df.loc[closest_index, 'SEM_STRIKE_PRICE']
				ce_df =ce_df[ce_df['SEM_STRIKE_PRICE']==strike]
			
			ce_df = ce_df.iloc[-1]	

			if pe_df.empty or len(pe_df)==0:
				pe_df['diff'] = abs(pe_df['SEM_STRIKE_PRICE'] - strike)
				closest_index = pe_df['diff'].idxmin()
				strike = pe_df.loc[closest_index, 'SEM_STRIKE_PRICE']
				pe_df =pe_df[pe_df['SEM_STRIKE_PRICE']==strike]
			
			pe_df = pe_df.iloc[-1]			

			ce_strike = ce_df['SEM_CUSTOM_SYMBOL']
			pe_strike = pe_df['SEM_CUSTOM_SYMBOL']

			if ce_strike== None:
				self.logger.info("No Scripts to Select from ce_spot_difference for ")
				return
			if pe_strike == None:
				self.logger.info("No Scripts to Select from pe_spot_difference for ")
				return
			
			return ce_strike, pe_strike, strike
		except Exception as e:
			traceback.print_exc()
			self.logger.exception("Got exception in ce_pe_option_df ", e)
			print('exception got in ce_pe_option_df',e)
			return None, None, strike

	def OTM_Strike_Selection(self, Underlying, Expiry,OTM_count=1):
		try:
			Expiry = pd.to_datetime(Expiry, format='%d-%m-%Y').strftime('%Y-%m-%d')
			exchange_index = {"BANKNIFTY": "NSE","NIFTY":"NSE","MIDCPNIFTY":"NSE", "FINNIFTY":"NSE","SENSEX":"BSE","BANKEX":"BSE"}
			instrument_df = self.instrument_df.copy()

			instrument_df['SEM_EXPIRY_DATE'] = pd.to_datetime(instrument_df['SEM_EXPIRY_DATE'], errors='coerce')
			instrument_df['ContractExpiration'] = instrument_df['SEM_EXPIRY_DATE'].dt.date
			instrument_df['ContractExpiration'] = instrument_df['ContractExpiration'].astype(str)

			if Underlying in exchange_index:
				exchange = exchange_index[Underlying]
			elif Underlying in self.commodity_step_dict.keys():
				exchange = "MCX"
			else:
				# exchange = instrument_df[((instrument_df['SEM_TRADING_SYMBOL']==Underlying)|(instrument_df['SEM_CUSTOM_SYMBOL']==Underlying))].iloc[0]['SEM_EXM_EXCH_ID']
				exchange = "NSE"
	
			ltp_data = self.get_ltp_data(Underlying)
			ltp = ltp_data[Underlying]
			if Underlying in self.index_step_dict:
				step = self.index_step_dict[Underlying]
			if Underlying in self.stock_step_df:
				step = self.stock_step_df[Underlying]
			if Underlying in self.commodity_step_dict:
				step = self.commodity_step_dict[Underlying]
			strike = round(ltp/step) * step
			

			if OTM_count<1:
				return "INVALID OTM DISTANCE"

			step = int(OTM_count*step)

			ce_OTM_price = strike+step
			pe_OTM_price = strike-step

			if exchange !="MCX":
				ce_condition = (instrument_df['SEM_EXM_EXCH_ID'] == exchange) & ((instrument_df['SEM_TRADING_SYMBOL'].str.contains(Underlying))|(instrument_df['SEM_CUSTOM_SYMBOL'].str.contains(Underlying))) & (instrument_df['ContractExpiration'] == Expiry) & (instrument_df['SEM_OPTION_TYPE']=='CE') 
				pe_condition = (instrument_df['SEM_EXM_EXCH_ID'] == exchange) & ((instrument_df['SEM_TRADING_SYMBOL'].str.contains(Underlying))|(instrument_df['SEM_CUSTOM_SYMBOL'].str.contains(Underlying))) & (instrument_df['ContractExpiration'] == Expiry) & (instrument_df['SEM_OPTION_TYPE']=='PE')
			else: 		
				ce_condition = (instrument_df['SEM_EXM_EXCH_ID'] == exchange) & ((instrument_df['SEM_TRADING_SYMBOL'].str.contains(Underlying))|(instrument_df['SEM_CUSTOM_SYMBOL'].str.contains(Underlying))) & (instrument_df['ContractExpiration'] == Expiry) & (instrument_df['SEM_OPTION_TYPE']=='CE') & (instrument_df['SM_SYMBOL_NAME']==Underlying) 
				pe_condition = (instrument_df['SEM_EXM_EXCH_ID'] == exchange) & ((instrument_df['SEM_TRADING_SYMBOL'].str.contains(Underlying))|(instrument_df['SEM_CUSTOM_SYMBOL'].str.contains(Underlying))) & (instrument_df['ContractExpiration'] == Expiry) & (instrument_df['SEM_OPTION_TYPE']=='PE')	& (instrument_df['SM_SYMBOL_NAME']==Underlying)			
			ce_df = instrument_df[ce_condition].copy()
			pe_df = instrument_df[pe_condition].copy()

			ce_df['SEM_STRIKE_PRICE'] = ce_df['SEM_STRIKE_PRICE'].astype("int")
			pe_df['SEM_STRIKE_PRICE'] = pe_df['SEM_STRIKE_PRICE'].astype("int")

			ce_df =ce_df[ce_df['SEM_STRIKE_PRICE']==ce_OTM_price]
			pe_df =pe_df[pe_df['SEM_STRIKE_PRICE']==pe_OTM_price]

			if ce_df.empty or len(ce_df)==0:
				ce_df['diff'] = abs(ce_df['SEM_STRIKE_PRICE'] - ce_OTM_price)
				closest_index = ce_df['diff'].idxmin()
				ce_OTM_price = ce_df.loc[closest_index, 'SEM_STRIKE_PRICE']
				ce_df =ce_df[ce_df['SEM_STRIKE_PRICE']==ce_OTM_price]
			
			ce_df = ce_df.iloc[-1]	

			if pe_df.empty or len(pe_df)==0:
				pe_df['diff'] = abs(pe_df['SEM_STRIKE_PRICE'] - pe_OTM_price)
				closest_index = pe_df['diff'].idxmin()
				pe_OTM_price = pe_df.loc[closest_index, 'SEM_STRIKE_PRICE']
				pe_df =pe_df[pe_df['SEM_STRIKE_PRICE']==pe_OTM_price]
			
			pe_df = pe_df.iloc[-1]			

			ce_strike = ce_df['SEM_CUSTOM_SYMBOL']
			pe_strike = pe_df['SEM_CUSTOM_SYMBOL']

			if ce_strike== None:
				self.logger.info("No Scripts to Select from ce_spot_difference for ")
				return
			if pe_strike == None:
				self.logger.info("No Scripts to Select from pe_spot_difference for ")
				return
			
			return ce_strike, pe_strike, ce_OTM_price, pe_OTM_price
		except Exception as e:
			print(f"Getting Error at OTM strike Selection as {e}")
			return None,None,0,0


	def ITM_Strike_Selection(self, Underlying, Expiry, ITM_count=1):
		try:
			Expiry = pd.to_datetime(Expiry, format='%d-%m-%Y').strftime('%Y-%m-%d')
			exchange_index = {"BANKNIFTY": "NSE","NIFTY":"NSE","MIDCPNIFTY":"NSE", "FINNIFTY":"NSE","SENSEX":"BSE","BANKEX":"BSE"}
			instrument_df = self.instrument_df.copy()

			instrument_df['SEM_EXPIRY_DATE'] = pd.to_datetime(instrument_df['SEM_EXPIRY_DATE'], errors='coerce')
			instrument_df['ContractExpiration'] = instrument_df['SEM_EXPIRY_DATE'].dt.date
			instrument_df['ContractExpiration'] = instrument_df['ContractExpiration'].astype(str)

			if Underlying in exchange_index:
				exchange = exchange_index[Underlying]
			elif Underlying in self.commodity_step_dict.keys():
				exchange = "MCX"
			else:
				# exchange = instrument_df[((instrument_df['SEM_TRADING_SYMBOL']==Underlying)|(instrument_df['SEM_CUSTOM_SYMBOL']==Underlying))].iloc[0]['SEM_EXM_EXCH_ID']
				exchange = "NSE"
	
			ltp_data = self.get_ltp_data(Underlying)
			ltp = ltp_data[Underlying]
			if Underlying in self.index_step_dict:
				step = self.index_step_dict[Underlying]
			if Underlying in self.stock_step_df:
				step = self.stock_step_df[Underlying]
			if Underlying in self.commodity_step_dict:
				step = self.commodity_step_dict[Underlying]
			strike = round(ltp/step) * step

			if ITM_count<1:
				return "INVALID ITM DISTANCE"
			
			step = int(ITM_count*step)
			ce_ITM_price = strike-step
			pe_ITM_price = strike+step

			if exchange !="MCX":
				ce_condition = (instrument_df['SEM_EXM_EXCH_ID'] == exchange) & ((instrument_df['SEM_TRADING_SYMBOL'].str.contains(Underlying))|(instrument_df['SEM_CUSTOM_SYMBOL'].str.contains(Underlying))) & (instrument_df['ContractExpiration'] == Expiry) & (instrument_df['SEM_OPTION_TYPE']=='CE') 
				pe_condition = (instrument_df['SEM_EXM_EXCH_ID'] == exchange) & ((instrument_df['SEM_TRADING_SYMBOL'].str.contains(Underlying))|(instrument_df['SEM_CUSTOM_SYMBOL'].str.contains(Underlying))) & (instrument_df['ContractExpiration'] == Expiry) & (instrument_df['SEM_OPTION_TYPE']=='PE')
			else: 		
				ce_condition = (instrument_df['SEM_EXM_EXCH_ID'] == exchange) & ((instrument_df['SEM_TRADING_SYMBOL'].str.contains(Underlying))|(instrument_df['SEM_CUSTOM_SYMBOL'].str.contains(Underlying))) & (instrument_df['ContractExpiration'] == Expiry) & (instrument_df['SEM_OPTION_TYPE']=='CE') & (instrument_df['SM_SYMBOL_NAME']==Underlying) 
				pe_condition = (instrument_df['SEM_EXM_EXCH_ID'] == exchange) & ((instrument_df['SEM_TRADING_SYMBOL'].str.contains(Underlying))|(instrument_df['SEM_CUSTOM_SYMBOL'].str.contains(Underlying))) & (instrument_df['ContractExpiration'] == Expiry) & (instrument_df['SEM_OPTION_TYPE']=='PE')	& (instrument_df['SM_SYMBOL_NAME']==Underlying)			
			ce_df = instrument_df[ce_condition].copy()
			pe_df = instrument_df[pe_condition].copy()

			ce_df['SEM_STRIKE_PRICE'] = ce_df['SEM_STRIKE_PRICE'].astype("int")
			pe_df['SEM_STRIKE_PRICE'] = pe_df['SEM_STRIKE_PRICE'].astype("int")

			ce_df =ce_df[ce_df['SEM_STRIKE_PRICE']==ce_ITM_price]
			pe_df =pe_df[pe_df['SEM_STRIKE_PRICE']==pe_ITM_price]

			if ce_df.empty or len(ce_df)==0:
				ce_df['diff'] = abs(ce_df['SEM_STRIKE_PRICE'] - ce_ITM_price)
				closest_index = ce_df['diff'].idxmin()
				ce_ITM_price = ce_df.loc[closest_index, 'SEM_STRIKE_PRICE']
				ce_df =ce_df[ce_df['SEM_STRIKE_PRICE']==ce_ITM_price]
			
			ce_df = ce_df.iloc[-1]	

			if pe_df.empty or len(pe_df)==0:
				pe_df['diff'] = abs(pe_df['SEM_STRIKE_PRICE'] - pe_ITM_price)
				closest_index = pe_df['diff'].idxmin()
				pe_ITM_price = pe_df.loc[closest_index, 'SEM_STRIKE_PRICE']
				pe_df =pe_df[pe_df['SEM_STRIKE_PRICE']==pe_ITM_price]
			
			pe_df = pe_df.iloc[-1]			

			ce_strike = ce_df['SEM_CUSTOM_SYMBOL']
			pe_strike = pe_df['SEM_CUSTOM_SYMBOL']

			if ce_strike== None:
				self.logger.info("No Scripts to Select from ce_spot_difference for ")
				return
			if pe_strike == None:
				self.logger.info("No Scripts to Select from pe_spot_difference for ")
				return
			
			return ce_strike, pe_strike, ce_ITM_price, pe_ITM_price
		except Exception as e:
			print(f"Getting Error at OTM strike Selection as {e}")
			return None,None,0,0

	def cancel_all_orders(self) -> dict:
		try:
			order_details=dict()
			product_detail ={'MIS':self.Dhan.INTRA, 'MARGIN':self.Dhan.MARGIN, 'MTF':self.Dhan.MTF, 'CO':self.Dhan.CO,'BO':self.Dhan.BO, 'CNC': self.Dhan.CNC}
			product = product_detail['MIS']
			time.sleep(1)
			data = self.Dhan.get_order_list()["data"]
			if data is None or len(data)==0:
				return order_details
			orders = pd.DataFrame(data)
			if orders.empty:
				return order_details
			trigger_pending_orders = orders.loc[(orders['orderStatus'] == 'PENDING') & (orders['productType'] == product)]
			open_orders = orders.loc[(orders['orderStatus'] == 'TRANSIT') & (orders['productType'] == product)]
			for index, row in trigger_pending_orders.iterrows():
				response = self.Dhan.cancel_order(row['orderId'])

			for index, row in open_orders.iterrows():
				response = self.Dhan.cancel_order(row['orderId'])
			position_dict = self.Dhan.get_positions()["data"]
			positions_df = pd.DataFrame(position_dict)
			if positions_df.empty:
				return order_details
			positions_df['netQty']=positions_df['netQty'].astype(int)
			bought = positions_df.loc[(positions_df['netQty'] > 0) & (positions_df["productType"] == product)]
			sold = positions_df.loc[(positions_df['netQty'] < 0) & (positions_df['productType'] == product)]

			for index, row in bought.iterrows():
				qty = int(row["netQty"])
				order = self.Dhan.place_order(security_id=str(row["securityId"]), exchange_segment=row["exchangeSegment"],
												transaction_type=self.Dhan.SELL, quantity=qty,
												order_type=self.Dhan.MARKET, product_type=row["productType"], price=0,
												trigger_price=0)

				tradingsymbol = row['tradingSymbol']
				sell_order_id= order["data"]["orderId"]
				order_details[tradingsymbol]=dict({'orderid':sell_order_id,'price':0})
				time.sleep(0.5)

			for index, row in sold.iterrows():
				qty = int(row["netQty"]) * -1
				order = self.Dhan.place_order(security_id=str(row["securityId"]), exchange_segment=row["exchangeSegment"],
												transaction_type=self.Dhan.BUY, quantity=qty,
												order_type=self.Dhan.MARKET, product_type=row["productType"], price=0,
												trigger_price=0)
				tradingsymbol = row['tradingSymbol']
				buy_order_id=order["data"]["orderId"]
				order_details[tradingsymbol]=dict({'orderid':buy_order_id,'price':0})
				time.sleep(1)
			if len(order_details)!=0:
				_,order_price = self.order_report()
				for key,value in order_details.items():
					orderid = str(value['orderid'])
					if orderid in order_price:
						order_details[key]['price'] = order_price[orderid] 	
			return order_details
		except Exception as e:
			print(e)
			print("problem close all trades")
			self.logger.exception("problem close all trades")
			traceback.print_exc()

	def order_report(self) -> Tuple[Dict, Dict]:
		'''
		If watchlist has more than two stock, using order_report, get the order status and order execution price
		order_report()
		'''
		try:
			order_details= dict()
			order_exe_price= dict()
			status_df = self.Dhan.get_order_list()["data"]
			status_df = pd.DataFrame(status_df)
			if not status_df.empty:
				status_df.set_index('orderId',inplace=True)
				order_details = status_df['orderStatus'].to_dict()
				order_exe_price = status_df['averageTradedPrice'].to_dict()
			
			return order_details, order_exe_price
		except Exception as e:
			self.logger.exception(f"Exception in getting order report as {e}")
			return dict(), dict()

	def get_order_detail(self,orderid:str, debug= "NO")->dict:
		try:
			orderid = str(orderid)
			response = self.Dhan.get_order_by_id(orderid)
			if debug.upper()=="YES":
				print(response)
			if response['status']=='success':
				return response['data'][0]
			else:
				raise Exception(response)
		except Exception as e:
			print(f"Error at getting order details as {e}")
			self.logger.error(f"Error at getting order details as {e}")
			return {
				'status':'failure',
				'remarks':str(e),
				'data':response,
			}

	
	def get_order_status(self, orderid:str, debug= "NO")->str:
		try:
			orderid = str(orderid)
			response = self.Dhan.get_order_by_id(orderid)
			if debug.upper()=="YES":
				print(response)			
			if response['status']=='success':
				return response['data'][0]['orderStatus']
			else:
				raise Exception(response)
		except Exception as e:
			print(f"Error at getting order status as {e}")
			self.logger.error(f"Error at getting order status as {e}")
			return {
				'status':'failure',
				'remarks':str(e),
				'data':response,
			}	


	def get_executed_price(self, orderid:str, debug= "NO")->int:
		try:
			orderid = str(orderid)
			response = self.Dhan.get_order_by_id(orderid)
			if debug.upper()=="YES":
				print(response)				
			if response['status']=='success':
				return response['data'][0]['averageTradedPrice']
			else:
				raise Exception(response)
		except Exception as e:
			print(f"Error at get_executed_price as {e}")
			self.logger.error(f"Error at get_executed_price as {e}")
			return {
				'status':'failure',
				'remarks':str(e),
				'data':response,
			}

	def get_exchange_time(self,orderid:str, debug= "NO")->str:
		try:
			orderid = str(orderid)
			response = self.Dhan.get_order_by_id(orderid)
			if debug.upper()=="YES":
				print(response)				
			if response['status']=='success':
				return response['data'][0]['exchangeTime']
			else:
				raise Exception(response)
		except Exception as e:
			print(f"Error at get_exchange_time as {e}")
			self.logger.error(f"Error at get_exchange_time as {e}")
			return {
				'status':'failure',
				'remarks':str(e),
				'data':response,
			}			

	def get_holdings(self, debug= "NO")->list:
		try:
			response = self.Dhan.get_holdings()
			if debug.upper()=="YES":
				print(response)				
			if response['status']=='success':
				return response['data']
			else:
				raise Exception(response)		
		except Exception as e:
			print(f"Error at getting Holdings as {e}")
			self.logger.exception(f"Error at getting Holdings as {e}")
			return {
				'status':'failure',
				'remarks':str(e),
				'data':response,
			}

	def get_positions(self, debug= "NO")->list:
		try:
			response = self.Dhan.get_positions()
			if debug.upper()=="YES":
				print(response)				
			if response['status']=='success':
				return response['data']
			else:
				raise Exception(response)		
		except Exception as e:
			print(f"Error at getting Positions as {e}")
			self.logger.exception(f"Error at getting Positions as {e}")
			return {
				'status':'failure',
				'remarks':str(e),
				'data':response,
			}			

	def get_orderbook(self, debug= "NO")->list:
		try:
			response = self.Dhan.get_order_list()
			if debug.upper()=="YES":
				print(response)				
			if response['status']=='success':
				return response['data']
			else:
				raise Exception(response)		
		except Exception as e:
			print(f"Error at get_orderbook as {e}")
			self.logger.exception(f"Error at get_orderbook as {e}")
			return {
				'status':'failure',
				'remarks':str(e),
				'data':response,
			}
	
	def get_trade_book(self, debug= "NO")->list:
		try:
			response = self.Dhan.get_order_list()
			if debug.upper()=="YES":
				print(response)			
			if response['status']=='success':
				return response['data']
			else:
				raise Exception(response)		
		except Exception as e:
			print(f"Error at get_trade_book as {e}")
			self.logger.exception(f"Error at get_trade_book as {e}")
			return {
				'status':'failure',
				'remarks':str(e),
				'data':response,
			}
		
		
	def get_option_greek(self, strike: int, expiry_date: str, asset: str, interest_rate: float, flag: str, scrip_type: str):
		try:
			expiry = pd.to_datetime(expiry_date, format='%d-%m-%Y').strftime('%Y-%m-%d')
			exchange_index = {"BANKNIFTY": "NSE", "NIFTY": "NSE", "MIDCPNIFTY": "NSE", "FINNIFTY": "NSE", "SENSEX": "BSE", "BANKEX": "BSE"}
			asset_dict = {'NIFTY BANK': "BANKNIFTY", "NIFTY 50": "NIFTY", 'NIFTY FIN SERVICE': 'FINNIFTY', 'NIFTY MID SELECT': 'MIDCPNIFTY', "SENSEX": "SENSEX", "BANKEX": "BANKEX"}

			if asset in asset_dict:
				inst_asset = asset_dict[asset]
			elif asset in asset_dict.values():
				inst_asset = asset
			else:
				inst_asset = asset

			# exchange = exchange_index[inst_asset]

			instrument_df = self.instrument_df.copy()
			instrument_df['SEM_EXPIRY_DATE'] = pd.to_datetime(instrument_df['SEM_EXPIRY_DATE'], errors='coerce')
			instrument_df['ContractExpiration'] = instrument_df['SEM_EXPIRY_DATE'].dt.date.astype(str)

			data = instrument_df[
				# (instrument_df['SEM_EXM_EXCH_ID'] == exchange) &
				((instrument_df['SEM_TRADING_SYMBOL'].str.contains(inst_asset)) | 
				 (instrument_df['SEM_CUSTOM_SYMBOL'].str.contains(inst_asset))) &
				(instrument_df['ContractExpiration'] == expiry) &
				(instrument_df['SEM_STRIKE_PRICE'] == strike) &
				(instrument_df['SEM_OPTION_TYPE']==scrip_type)
			]

			if data.empty:
				self.logger.error('No data found for the specified parameters.')
				return None

			script_list = data['SEM_CUSTOM_SYMBOL'].tolist()
			script = script_list[0]

			days_to_expiry = (datetime.datetime.strptime(expiry_date, "%d-%m-%Y").date() - datetime.datetime.now().date()).days
			if days_to_expiry <= 0:
				days_to_expiry = 1

			ltp_data = self.get_ltp_data([asset,script])
			asset_price = ltp_data[asset]
			ltp = ltp_data[script]
			# asset_price = self.get_ltp(asset)
			# ltp = self.get_ltp(script)

			if scrip_type == 'CE':
				civ = mibian.BS([asset_price, strike, interest_rate, days_to_expiry], callPrice= ltp)
				cval = mibian.BS([asset_price, strike, interest_rate, days_to_expiry], volatility = civ.impliedVolatility ,callPrice= ltp)
				if flag == "price":
					return cval.callPrice
				if flag == "delta":
					return cval.callDelta
				if flag == "delta2":
					return cval.callDelta2
				if flag == "theta":
					return cval.callTheta
				if flag == "rho":
					return cval.callRho
				if flag == "vega":
					return cval.vega
				if flag == "gamma":
					return cval.gamma
				if flag == "all_val":
					return {'callPrice' : cval.callPrice, 'callDelta' : cval.callDelta, 'callDelta2' : cval.callDelta2, 'callTheta' : cval.callTheta, 'callRho' : cval.callRho, 'vega' : cval.vega, 'gamma' : cval.gamma}

			if scrip_type == "PE":
				piv = mibian.BS([asset_price, strike, interest_rate, days_to_expiry], putPrice= ltp)
				pval = mibian.BS([asset_price, strike, interest_rate, days_to_expiry], volatility = piv.impliedVolatility ,putPrice= ltp)
				if flag == "price":
					return pval.putPrice
				if flag == "delta":
					return pval.putDelta
				if flag == "delta2":
					return pval.putDelta2
				if flag == "theta":
					return pval.putTheta
				if flag == "rho":
					return pval.putRho
				if flag == "vega":
					return pval.vega
				if flag == "gamma":
					return pval.gamma
				if flag == "all_val":
					return {'callPrice' : pval.putPrice, 'callDelta' : pval.putDelta, 'callDelta2' : pval.putDelta2, 'callTheta' : pval.putTheta, 'callRho' : pval.putRho, 'vega' : pval.vega, 'gamma' : pval.gamma}

		except Exception as e:
			self.logger.exception(f"Exception in get_option_greek: {e}")
			return None








	# def kill_switch(self,status):
	# 	active = {'ON':'ACTIVATE','OFF':'DEACTIVATE'}
	# 	current_status = active[status.upper()]
	# 	killswitch_url = "https://api.dhan.co/killSwitch"
	# 	params = {
	# 	"killSwitchStatus":current_status, #DEACTIVATE	
	# 	"access-token":self.token_id

	# 	}
	# 	headers = {
	# 		"Content-Type": "application/json",
	# 		"access-token":self.token_id
	# 	}

	# 	killswitch_response = requests.post(killswitch_url, headers=headers, params=params)

	# 	if 'killSwitchStatus' in killswitch_response.json().keys():
	# 		return killswitch_response.json()['killSwitchStatus']
	# 	else:
	# 		return killswitch_response.json()


	# def get_historical_data(self,tradingsymbol,exchange,interval,start,end):
	# 	"""Retrieve OHLC & Volume of 1 minute candle for desired instrument for current day. This data available for all segments including futures & options."""
	# 	try:
	# 		# script_exchange = {"NSE":self.Dhan.NSE, "NFO":self.Dhan.NSE_FNO, "BFO":self.Dhan.BSE_FNO, "CUR": self.Dhan.CUR, "BSE":self.Dhan.BSE, "MCX":self.Dhan.MCX}
	# 		script_exchange = {"NSE":self.Dhan.NSE, "NFO":self.Dhan.FNO, "BFO":self.Dhan.FNO, "CUR": self.Dhan.CUR, "BSE":self.Dhan.BSE, "MCX":self.Dhan.MCX, "IDX_I":self.Dhan.INDEX}
	# 		instrument_exchange = {'NSE':"NSE",'BSE':"BSE",'NFO':'NSE','BFO':'BSE','MCX':'MCX','CUR':'NSE'}
	# 		exchange_segment = script_exchange[exchange]
	# 		index_exchange = {"NIFTY":'NSE',"BANKNIFTY":"NSE","FINNIFTY":"NSE","MIDCPNIFTY":"NSE","BANKEX":"BSE","SENSEX":"BSE"}
	# 		if tradingsymbol in index_exchange:
	# 			exchange =index_exchange[tradingsymbol]
	# 		security_id = self.instrument_df[((self.instrument_df['SEM_TRADING_SYMBOL']==tradingsymbol)|(self.instrument_df['SEM_CUSTOM_SYMBOL']==tradingsymbol))&(self.instrument_df['SEM_EXM_EXCH_ID']==instrument_exchange[exchange])].iloc[-1]['SEM_SMST_SECURITY_ID']
	# 		instrument_type = self.instrument_df[((self.instrument_df['SEM_TRADING_SYMBOL']==tradingsymbol)|(self.instrument_df['SEM_CUSTOM_SYMBOL']==tradingsymbol))&(self.instrument_df['SEM_EXM_EXCH_ID']==instrument_exchange[exchange])].iloc[-1]['SEM_INSTRUMENT_NAME']

	# 		url= 'https://api.dhan.co/v2/charts/intraday'
	# 		payload= {'securityId':str(security_id),'exchangeSegment':exchange_segment,'instrument':instrument_type,"interval":interval,"fromDate": start,"toDate": end}

	# 		header = {
	# 			"Content-Type": "application/json",
	# 			"access-token":self.token_id
	# 		}
	# 		payload= json_dumps(payload)
	# 		response= requests.post(url,headers=header,timeout=60,data=payload)
	# 		ohlc = response.json()
	# 		if len(ohlc)!=0:
	# 			df = pd.DataFrame(ohlc)
	# 			if not df.empty:
	# 				df['timestamp'] = df['timestamp'].apply(lambda x: self.convert_to_date_time(x))
	# 				# df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s').dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata')
	# 				return df
	# 			else:
	# 				return pd.DataFrame()
	# 		else:
	# 			return pd.DataFrame()

	# 	except Exception as e:
	# 		self.logger.error('Exception in dhanhq>>intraday_daily_minute_charts: %s',e)
			# return {
			# 	'status':'failure',
			# 	'remarks':str(e),
			# 	'data':'',
			# }	


	# def get_historical_data(self,tradingsymbol,exchange,interval,start,end):
	# 	"""Retrieve OHLC & Volume of 1 minute candle for desired instrument for current day. This data available for all segments including futures & options."""
	# 	try:
	# 		# script_exchange = {"NSE":self.Dhan.NSE, "NFO":self.Dhan.NSE_FNO, "BFO":self.Dhan.BSE_FNO, "CUR": self.Dhan.CUR, "BSE":self.Dhan.BSE, "MCX":self.Dhan.MCX}
	# 		script_exchange = {"NSE":self.Dhan.NSE, "NFO":self.Dhan.FNO, "BFO":self.Dhan.FNO, "CUR": self.Dhan.CUR, "BSE":self.Dhan.BSE, "MCX":self.Dhan.MCX, "IDX_I":self.Dhan.INDEX}
	# 		instrument_exchange = {'NSE':"NSE",'BSE':"BSE",'NFO':'NSE','BFO':'BSE','MCX':'MCX','CUR':'NSE'}
	# 		exchange_segment = script_exchange[exchange]
	# 		index_exchange = {"NIFTY":'NSE',"BANKNIFTY":"NSE","FINNIFTY":"NSE","MIDCPNIFTY":"NSE","BANKEX":"BSE","SENSEX":"BSE"}
	# 		if tradingsymbol in index_exchange:
	# 			exchange =index_exchange[tradingsymbol]			
	# 		security_id = self.instrument_df[((self.instrument_df['SEM_TRADING_SYMBOL']==tradingsymbol)|(self.instrument_df['SEM_CUSTOM_SYMBOL']==tradingsymbol))&(self.instrument_df['SEM_EXM_EXCH_ID']==instrument_exchange[exchange])].iloc[-1]['SEM_SMST_SECURITY_ID']
	# 		instrument_type = self.instrument_df[((self.instrument_df['SEM_TRADING_SYMBOL']==tradingsymbol)|(self.instrument_df['SEM_CUSTOM_SYMBOL']==tradingsymbol))&(self.instrument_df['SEM_EXM_EXCH_ID']==instrument_exchange[exchange])].iloc[-1]['SEM_INSTRUMENT_NAME']
	# 		if interval in [1, 5, 15, 25, 60]:
	# 			pass
	# 		else:
	# 			raise Exception("interval value must be ['1','5','15','25','60']")
	# 		ohlc = self.Dhan.intraday_minute_data(str(security_id),exchange_segment,instrument_type,start,end,int(interval))
	# 		if len(ohlc['data'])!=0:
	# 			df = pd.DataFrame(ohlc['data'])
	# 			if not df.empty:
	# 				df['timestamp'] = df['timestamp'].apply(lambda x: self.convert_to_date_time(x))
	# 				# df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s').dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata')
	# 				return df
	# 			else:
	# 				return pd.DataFrame()
	# 		else:
	# 			return pd.DataFrame()

	# 	except Exception as e:
	# 		self.logger.error('Exception in dhanhq>>intraday_daily_minute_charts: %s',e)
	# 		return {
	# 			'status':'failure',
	# 			'remarks':str(e),
	# 			'data':'',
	# 		}



	# def get_ltp(self,name):
	# 	try:
	# 		exchange_index = {"BANKNIFTY": "NSE_IDX","NIFTY":"NSE_IDX","MIDCPNIFTY":"NSE_IDX", "FINNIFTY":"NSE_IDX","SENSEX":"BSE_IDX","BANKEX":"BSE_IDX"}
	# 		NFO = ["BANKNIFTY","NIFTY","MIDCPNIFTY","FINNIFTY"]
	# 		BFO = ['SENSEX','BANKEX']
	# 		equity = ['CALL','PUT','FUT']
	# 		if type(name)!=list:
	# 			if name in self.commodity_step_dict.keys():
	# 				name = instrument_df[(instrument_df['SEM_EXM_EXCH_ID']=='MCX')&(instrument_df['SM_SYMBOL_NAME']==name.upper())&(instrument_df['SEM_INSTRUMENT_NAME']=='FUTCOM')].sort_values(by='SEM_EXPIRY_DATE').iloc[0]['SEM_CUSTOM_SYMBOL']
	# 			nfo_check = ['NFO' for nfo in NFO if nfo in name]
	# 			bfo_check = ['BFO' for bfo in BFO if bfo in name]
	# 			exchange_nfo ='NFO' if len(nfo_check)!=0 else False
	# 			exchange_bfo = 'BFO' if len(bfo_check)!=0 else False
	# 			if not exchange_nfo and not exchange_bfo:
	# 				eq_check =['NFO' for nfo in equity if nfo in name]
	# 				exchange_eq ='NFO' if len(eq_check)!=0 else "NSE"
	# 			else:
	# 				exchange_eq="NSE"
	# 			exchange ='NFO' if exchange_nfo else ('BFO' if exchange_bfo else exchange_eq)
	# 			trail_exchange = exchange
	# 			mcx_check = ['MCX' for mcx in self.commodity_step_dict.keys() if mcx in name]
	# 			exchange = "MCX" if len(mcx_check)!=0 else exchange
	# 			if exchange == "MCX": 
	# 				if instrument_df[((instrument_df['SEM_CUSTOM_SYMBOL']==name)|(instrument_df['SEM_TRADING_SYMBOL']==name))&(instrument_df['SEM_EXM_EXCH_ID']=='MCX')].empty:
	# 					exchange = trail_exchange
	# 			name = [name]
	# 			df = self.sheet.range('A1').expand().options(pd.DataFrame, header=1, index=False).value
	# 			data = df[df['Script Name'].isin(name)]
	# 			if data.empty:
	# 				new_name = self.instrument_df[((self.instrument_df['SEM_CUSTOM_SYMBOL']==name[0])|(self.instrument_df['SEM_TRADING_SYMBOL']==name[0]))].iloc[-1]['SEM_TRADING_SYMBOL']
	# 				new_name = [new_name]
	# 				df = self.sheet.range('A1').expand().options(pd.DataFrame, header=1, index=False).value
	# 				data = df[df['Script Name'].isin(new_name)]
	# 			if data.empty:
	# 				df = self.sheet.range('A1').expand().options(pd.DataFrame, header=1, index=False).value
	# 				if len(df)<100:
	# 					add = list()
	# 					row = len(df)+2
	# 					add.extend(name)
	# 					add.append(exchange)
	# 					self.sheet.range(f'A{row}').value = add
	# 					df = self.sheet.range('A1').expand().options(pd.DataFrame, header=1, index=False).value
	# 					data = df[df['Script Name'].isin(name)]
	# 					check = data.fillna('0').iloc[-1]['LTP']=='0'
	# 					while check:
	# 						df = self.sheet.range('A1').expand().options(pd.DataFrame, header=1, index=False).value
	# 						data = df[df['Script Name'].isin(name)]
	# 						check = data.fillna('0').iloc[-1]['LTP']=='0'
	# 			data = data.set_index('Script Name')['LTP']
	# 			return data.to_dict()[name[0]] if name[0] in data else data.to_dict()[new_name[0]]
	# 		df = self.sheet.range('A1').expand().options(pd.DataFrame, header=1, index=False).value
	# 		data = df[df['Script Name'].isin(name)]
	# 		data = data.set_index('Script Name')['LTP']
	# 		return data.to_dict()
	# 	except Exception as e:
	# 		print(e)
	# 		self.logger.exception(f"Exception in getting LTP as {e}")
	# 		return 0

	def get_expiry(self,underlying):
		try:
			instrument_df = self.instrument_df.copy()	
			data = instrument_df[instrument_df['Name']==underlying].sort_values('ContractExpiration')
			data = pd.DataFrame(pd.to_datetime(data[data['ContractExpiration']!='1']['ContractExpiration']).dt.date.unique(),columns=['Expiry Dates'])
			
			if not data.empty:
				return data['Expiry Dates'].to_list()
			else:
				raise TypeError("check input parameter correctly for get_atm()")
		except Exception as e:
			print(f"Exception in get_expiry as: {e}")
			self.logger.exception(f"Exception in get_expiry as: {e}")
			return None

	def check_expiry_date(self,underlying,Expiry):
		try:
			data = self.instrument_df[self.instrument_df['Name']==underlying].sort_values('ContractExpiration')
			date = pd.to_datetime(data[data['ContractExpiration']!='1']['ContractExpiration']).dt.date.unique()
			if Expiry in date:
				return True
			else:
				return False
		except Exception as e:
			print(f"Exception in check_expiry_date as: {e}")
			self.logger.exception(f"Exception in check_expiry_date as: {e}")

	
	def get_freeze_quantity(self,strike):
		data =  self.instrument_df[(self.instrument_df['Description'] == strike)]
		if len(data) == 0:
			self.logger.exception("Enter valid Script Name")
			return 0
		else:
			return data.iloc[0]['FreezeQty']
	
	def get_split_order_variables(self,strike,lots):
		try:
			lot_size = self.get_lot_size(strike)
			quantity = lots*lot_size

			freeze_quantity = self.get_freeze_quantity(strike)
			split_count = quantity//freeze_quantity
			remain_quantity = quantity%freeze_quantity

			return quantity, freeze_quantity, split_count, remain_quantity		
		except Exception as e:
			print(e)
			self.logger.exception(f"Error in getting split order variables as {e}")
			return 0,0,0,0	
	

	def get_bid_ask(self,name):
		try:
			strike_exchange = self.instrument_df.loc[self.instrument_df['Description']==name].iloc[0][['ExchangeSegment']][0]
			data = instrument_df.loc[(instrument_df['ExchangeSegment'] == strike_exchange) & (instrument_df['Description'] == name)]
			exchangeInstrumentID = data.iloc[0]['ExchangeInstrumentID']
			exchange_dict = {"NSECM": 1, "NSEFO": 2, "NSECD": 3, "BSECM": 11, "BSEFO": 12}
			exchangeSegment = exchange_dict[strike_exchange]
			instruments = [{'exchangeSegment': int(exchangeSegment), 'exchangeInstrumentID': int(exchangeInstrumentID)}]
			ltp_quote = self.xts2.get_quote(Instruments=instruments, xtsMessageCode=1501, publishFormat='JSON')
			ask = json.loads(ltp_quote['result']['listQuotes'][-1])['AskInfo']['Price']
			bid = json.loads(ltp_quote['result']['listQuotes'][-1])['BidInfo']['Price']
			return ask,bid
		except Exception as e:
			print(e)
			self.logger.exception(f'get exception get_bid_ask function as {e} ')
			traceback.print_exc()


	def get_data_for_single_script(self,names:list) -> dict:
		try:
			instruments = []
			if type(names)!=list:
				names = [names]	
			for name in names:
				try:
					if (name in self.token_dict) and (name not in self.token_and_exchange):
						token 										= self.token_dict[name]['token']
						token_exchange 								= self.token_dict[name]['exchange']
						self.token_and_exchange[name] 				= {'token':token,'token_exchange':token_exchange}
					elif name not in self.token_and_exchange:
						token                                       = self.instrument_df.loc[self.instrument_df['Description']==name].iloc[0][['ExchangeInstrumentID']][0]
						token_exchange                              = self.instrument_df.loc[self.instrument_df['Description']==name].iloc[0][['ExchangeSegment']][0]
						self.token_and_exchange[name] 				= {'token':token,'token_exchange':token_exchange}
					else:
						token 										= self.token_and_exchange[name]['token']
						token_exchange 								= self.token_and_exchange[name]['token_exchange']
				except:
					print(f'{name} is not correct!! Check spelling')
					names.remove(name)
					continue
				instrument 									= {'exchangeSegment': str(self.segment_dict[token_exchange]), 'exchangeInstrumentID': str(token)}
				instruments.append(instrument)
			response = self.xts2.get_quote(Instruments=instruments, xtsMessageCode=1501, publishFormat='JSON')
			return response
		except Exception as e:
			print(e)
			self.logger.exception(f"Exception in getting get data for single script as {e}")
			traceback.print_exc()
			
	def get_stock_data(self,names:list) -> dict:
		'''
		For getting LTP, OPEN, HIGH, LOW, CLOSE Values for more than two tradingsymbol
		get_stock_data(stock_list)
		'''
		try:
			stock_data = dict()
			quote_dict = self.get_quote(names)
			if len(quote_dict)==0:
				return stock_data
			for stock in names:	
				if stock in quote_dict:			
					ltp 	= quote_dict[stock]['LastTradedPrice']				
					open 	= quote_dict[stock]['Open']
					high 	= quote_dict[stock]['High']
					low 	= quote_dict[stock]['Low']
					close 	= quote_dict[stock]['Close']
					stock_data[stock] = {'ltp':ltp,'open':open, 'high':high, 'low':low, 'close':close}
				else:
					stock_data[stock] = {'ltp':0,'open':0, 'high':0, 'low':0, 'close':0}
			
			return stock_data
		except Exception as e:
			self.logger.exception(f"Exceptionn in getting stock data as {e}")
			return dict()

	

	def get_quote(self,names):
		try:
			response = self.get_data_for_single_script(names)
			i=0
			result = {}
			if response:
				if type(names)==list:
					for i,data in enumerate(response['result']['listQuotes']):
						data = json.loads(data)
						name = self.instrument_df.loc[self.instrument_df['ExchangeInstrumentID'] == data['ExchangeInstrumentID']].iloc[0]['Description']
						result[name] = data
					return result
				else:
					data    = response['result']['listQuotes'][0]
					data    = json.loads(data)
					return data
			else:
				print('No data returned from XTS')
				return None
		except Exception as e:
			print(e)
			self.logger.exception(f"Exception in get quote function as {e}")
			traceback.print_exc()



	def get_orderhistory(self, order_id):
		try:
			flag = True
			while flag == True:
				try:
					time.sleep(1)
					order_history = self.xts1.get_order_history(appOrderID=order_id,clientID=self.client_code)
					send_order_history = order_history['result'][-1]
					flag = False
				except Exception as e:
					pass
			return send_order_history['OrderStatus']
		except Exception as e:
			self.logger.exception("exception in get_orderhistory {0} ".format(str(e)))

	def modify_order(self,appOrderID:str,modifiedOrderType:str, modifiedOrderQuantity:int, modifiedLimitPrice:int, modifiedStopPrice:int, trade_type:str) -> str:
		try:
			p_orders = pd.DataFrame(self.xts1.get_order_book()['result'])
			before_len = len(p_orders)
			self.order_Type = {'LIMIT': self.xts1.ORDER_TYPE_LIMIT, 'MARKET': self.xts1.ORDER_TYPE_MARKET,'STOPLIMIT': self.xts1.ORDER_TYPE_STOPLIMIT, 'STOPMARKET': self.xts1.ORDER_TYPE_STOPMARKET}
			product = {'MIS': self.xts1.PRODUCT_MIS, 'NRML': self.xts1.PRODUCT_NRML, 'CNC': 'CNC'}
			Validity = {'DAY': self.xts1.VALIDITY_DAY, 'IOC': 'IOC'}


			product_Type = product[trade_type.upper()]
			order_type = self.order_Type[modifiedOrderType.upper()]
			time_in_force = Validity['DAY']

			order = self.xts1.modify_order(appOrderID=appOrderID,modifiedProductType=product_Type,modifiedOrderType=order_type,modifiedOrderQuantity=modifiedOrderQuantity,modifiedDisclosedQuantity=0,modifiedLimitPrice=modifiedLimitPrice,modifiedStopPrice=modifiedStopPrice,modifiedTimeInForce=time_in_force,orderUniqueIdentifier="123abc")
			order_id = order['result']['AppOrderID']
			# time.sleep(1)
			c_orders = pd.DataFrame(self.xts1.get_order_book()['result'])
			after_len = len(c_orders)
			if order_id == None:
				print("didnt find order id from api trying to get it via wrapper")
				if before_len < after_len:
					order_id = c_orders.iloc[-1]['order_id']
					return order_id
			else:
				return str(order_id)
		except Exception as e:
			self.logger.exception(f'Got exception in modify_order as {e}')
			traceback.print_exc()

	def cancel_order(self,OrderID:str)->None:
		try:
			response = self.xts1.cancel_order(appOrderID=OrderID,orderUniqueIdentifier='123abc',clientID=self.client_code)
		except Exception as e:
			self.logger.exception(f'Got exception in cancel_order as {e}')
			traceback.print_exc()

	def check_valid_instrument(self,name):
		try:
			df = self.instrument_df[(self.instrument_df['Description']==name) | (self.instrument_df['Name']==name)]
			if len(df) != 0:
				return f"instrument {name} is valid"
			else:
				return f"instrument {name} is invalid"

		except Exception as e:
			print(e)
			self.logger.exception(f'Exception at check valid instrument as {e}')
			traceback.print_exc()
			return f"instrument {name} is invalid"

	def send_telegram_alert(self,message,receiver_chat_id,bot_token=None):
		"""
			1st receiver need to connect with BOT TradeHull Bot token is "5189311784:AAHgQxiQ6uhc1Qf7AvPAiUoUzxetu8uKP58" 
		"""
		try:
			bot_token = "5189311784:AAHgQxiQ6uhc1Qf7AvPAiUoUzxetu8uKP58"
			send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + receiver_chat_id + '&text=' + message
			response = requests.get(send_text)
		except Exception as e:
			print(e)
			self.logger.exception(f"Exception in sending telegram alerts as {e}")
			traceback.print_exc()
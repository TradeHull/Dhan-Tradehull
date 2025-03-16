import pandas as pd
import datetime
import pdb
import math


def market_type(num):
	if num > 1.47:
		return "very_bullish"

	if 0.75 < num < 1.46:
		return "bullish"

	if 0 < num < 0.74:
		return "neutral"

	if -0.7 < num < 0:
		return "bearish"

	if num <= -0.7:
		return "very_bearish"


def sqn(df, period):
	df['pnl_sqn'] = ((df['close'] - df['open']) / df['open'])*100
	df['average_pnl'] = df['pnl_sqn'].rolling(period).mean()
	df['average_std'] = df['pnl_sqn'].rolling(period).std()
	name = 'sqn'
	df[name] = (math.sqrt(period)*df['average_pnl'])/df['average_std']
	df = df.drop(columns=['pnl_sqn', 'average_pnl', 'average_std'], inplace=True)
	return df



# Implementation
# sqn_lib.sqn(df=df, period=21)
# df['market_type'] = df['sqn'].apply(sqn_lib.market_type)

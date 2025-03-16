Stock Option Algo

Pre Market scanning

	Use Nifty 50 for pre market scanning
	Select script that has the highest body_percentage
	mark high for entry level when candle is_ green
	mark low  for entry level when candle is_ red

Entry
	Wait for the candle to close above high or low
	Check if the candle has 2X of average volume
	Check if candle is not doji

Trade
	Get atm options name
	get ltp atm options name
	get lot size for atm options name
	entry
	keep a  sl of 20%

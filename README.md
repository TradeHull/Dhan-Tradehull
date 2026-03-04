# TradeHull Dhan Codebase Project

This project is built to interact with the **Dhan API** using the `Dhan_Tradehull` library. It provides a comprehensive suite of tools for trading, fetching market data, placing orders, and analyzing options.

---

## Features
- **Fetch Market Data**: Get Live Trading Price (LTP), historical data.
- **Order Placement**: Place, modify, or cancel orders with various parameters.
- **Option Greeks**: Retrieve Greeks like Delta, Theta, Gamma, and Vega for options.
- **Option Strike Selection**: Automate ATM, ITM, and OTM strike price identification.
- **Portfolio Management**: Fetch holdings, positions, and balances.
- **Option Chain**: Retrieve and analyze option chain data.
- **Advanced Order Types**: Supports sliced orders, bracket orders, and stop-loss orders.

---


## Installation

To install Dhan package 
```python 
pip install Dhan-Tradehull
```
Install required dependencies
```python 
pip install -r requirement.txt
```
## Upgrade Dhan Package

To update the Dhan package
```python
pip install --upgrade Dhan-Tradehull 
```

## Usage

### Dhan API Authentication

`Dhan_Tradehull` now supports **three** authentication modes:

- `access_token` - Login using Client Code + Access Token
- `api_key` - Login using Client Code + API Key + API Secret
- `pin_totp` - Login using Client Code + PIN + TOTP Secret

---

### 1) Access Token Login (`mode="access_token"`)

```python
from Dhan_Tradehull import Tradehull

client_code = "your_client_code"
token_id    = "your_access_token"

tsl = Tradehull(client_code, token_id, mode="access_token")
```

### 2) API Key Login (`mode="api_key"`)

This method uses a browser-based authorization flow:

1. The library opens a browser window.
2. Login with your Dhan credentials.
3. After successful login, you will be redirected to a URL containing a token.
4. Copy that full redirected URL and paste it into the terminal when prompted.

```python
from Dhan_Tradehull import Tradehull

client_code = "your_client_code"
api_key     = "your_api_key"
api_secret  = "your_api_secret"

tsl = Tradehull(client_code, mode="api_key", api_key=api_key, api_secret=api_secret)
```

### 3) PIN + TOTP Login (`mode="pin_totp"`)

```python
from Dhan_Tradehull import Tradehull

client_code  = "your_client_code"
pin          = "your_pin"
totp_secret  = "your_totp_secret"

tsl = Tradehull(ClientCode=client_code, mode="pin_totp", pin=pin, totp_secret=totp_secret)
```


## Key Functionalities

1. **Fetch Live Market Data**

   Get the latest trading price (LTP) or quote data:

   *Get LTP*

      - tsl.get_ltp_data(names: list or str, debug: str = "NO")

      - Arguments:
         - names (list or str): List of instrument names or a single instrument name to fetch the LTP.
         - debug (optional, str): Set to "YES" to enable detailed API response logging. Default is "NO".

      - Sample Code:
         ```python
            data = tsl.get_ltp_data(names=['CRUDEOIL', 'NIFTY'])
            crudeoil_ltp = data['CRUDEOIL']
         ```
   
   *Get Quotes*

      - tsl.get_quote_data(names: list or str, debug: str = "NO")

      - Arguments:
         - names (list or str): List of instrument names or a single instrument name to fetch the Quote data.
         - debug (optional, str): Set to "YES" to enable detailed API response logging. Default is "NO".

      - Sample Code:
         ```python
            data = tsl.get_quote_data(names=['CRUDEOIL', 'NIFTY'])
            crudeoil_quote_data = data['CRUDEOIL']
         ```
   
   *Get OHLC*

      - tsl.get_ohlc_data(names: list or str, debug: str = "NO")

      - Arguments:
         - names (list or str): List of instrument names or a single instrument name to fetch the OHLC data.
         - debug (optional, str): Set to "YES" to enable detailed API response logging. Default is "NO".

      - Sample Code:
         ```python
            data = tsl.get_ohlc_data(names=['CRUDEOIL', 'NIFTY'])
            crudeoil_ohlc_data = data['CRUDEOIL']
         ```   

---

2. **Fetch Historical Data**

   *Get Historical Data*
   
      - tsl.get_historical_data(tradingsymbol: str, exchange: str, timeframe: str, sector: str = "NO", debug: str = "NO")

         - Arguments:
            - tradingsymbol (str): The trading symbol for the instrument you want to fetch data for (e.g., 'NIFTY', 'ACC').
            - exchange (str): The exchange where the instrument is traded (e.g., 'NSE', 'INDEX').
            - timeframe (str): The timeframe for the data. It can be:
               - '1' for 1-minute candles
               - '5' for 5-minute candles
               - '15' for 15-minute candles
               - '25' for 25-minute candles
               - '60' for 60-minute candles
               - 'DAY' for daily candles
            - sector (optional, str): Set to "YES" to fetch sector data(e.g., 'Nifty Healthcare', 'NIFTY 100'). Default is "NO".
            - debug (optional, str): Set to "YES" to enable detailed API response logging. Default is "NO".
         
         - Sample Code:
            ```python
               data = tsl.get_historical_data(tradingsymbol='NIFTY', exchange='INDEX', timeframe="DAY")
               data = tsl.get_historical_data(tradingsymbol='ACC', exchange='NSE', timeframe="1")
               # sector data
               data = tsl.get_historical_data(tradingsymbol="NIFTY 100", exchange="NSE", timeframe="DAY", sector="YES")
            ```

   *Get Long-Term Historical Data*

      - tsl.get_long_term_historical_data(tradingsymbol: str, exchange: str, timeframe: str, from_date: str, to_date: str, sector: str = "NO", debug: str = "NO")

      - Arguments:
         - tradingsymbol (str): The trading symbol for the instrument you want to fetch data for (e.g., 'RELIANCE', 'NIFTY', 'CRUDEOIL').
         - exchange (str): The exchange where the instrument is traded (e.g., 'NSE', 'INDEX', 'MCX').
         - timeframe (str): The timeframe for the data. It can be:
            - '1' for 1-minute candles
            - '5' for 5-minute candles
            - '15' for 15-minute candles
            - '25' for 25-minute candles
            - '60' for 60-minute candles
            - 'DAY' for daily candles
         - from_date (str): Start date for fetching data (format: YYYY-MM-DD).
         - to_date (str): End date for fetching data (format: YYYY-MM-DD).
         - sector (optional, str): Set to "YES" to fetch sector data(e.g., 'Nifty Healthcare', 'NIFTY 100'). Default is "NO".
         - debug (optional, str): Set to "YES" to enable detailed API response logging. Default is "NO".

      - Sample Code:
         ```python
         data = tsl.get_long_term_historical_data(tradingsymbol='RELIANCE',exchange='NSE',timeframe='5',from_date='2021-01-01',to_date='2025-10-17')
         # sector data
         data = tsl.get_long_term_historical_data(tradingsymbol="NIFTY 100", exchange="NSE", timeframe="5", from_date="2022-01-01", to_date="2025-12-03", sector="YES")
         
         ```


3. **Option Strike Selection**

   ATM/ITM/OTM strike selection:

   *Get ATM Strikes*

      - tsl.ATM_Strike_Selection(Underlying: str, Expiry: int)

      - Arguments:
         - Underlying (str): The index or instrument name for which you want to find the ATM strike prices (e.g., 'NIFTY', 'BANKNIFTY').
         - Expiry (int): The expiry to select. 
            - 0 - Current week/month (depending on expiry type)
            - 1 - Next week/month (depending on expiry type)
            - and so on for subsequent weeks/months.

      -  Returns:
         - CE_symbol_name (str): The option symbol for the Call strike.
         - PE_symbol_name (str): The option symbol for the Put strike.
         - strike (int): The ATM strike price.

      - Sample Code:         
         ```python      
            CE_symbol_name, PE_symbol_name, strike = tsl.ATM_Strike_Selection(Underlying='NIFTY', Expiry=0)
         ```
      


   *Get OTM Strikes*

      - tsl.OTM_Strike_Selection(Underlying: str, Expiry: int, OTM_count: int)

      - Arguments:
         - Underlying (str): The index or instrument name for which you want to find the OTM strike prices (e.g., 'NIFTY', 'BANKNIFTY').
         - Expiry (int): The expiry to select. 
            - 0 - Current week/month (depending on expiry type)
            - 1 - Next week/month (depending on expiry type)
            - and so on for subsequent weeks/months.
         - OTM_count (int): The number of steps to move away from the ATM strike to find the OTM strike prices (e.g., 5 means 5 steps away).

      - Returns:
         - CE_symbol_name (str): The option symbol for the OTM Call strike.
         - PE_symbol_name (str): The option symbol for the OTM Put strike.
         - CE_strike (int): The OTM Call strike price.
         - PE_strike (int): The OTM Put strike price.

      - Sample Code:         
         ```python      
            CE_symbol_name, PE_symbol_name, CE_strike, PE_strike = tsl.OTM_Strike_Selection(Underlying='NIFTY', Expiry=0, OTM_count=5)
         ```      

   

   *Get ITM Strikes*

      - tsl.ITM_Strike_Selection(Underlying: str, Expiry: int, ITM_count: int)

      - Arguments:
         - Underlying (str): The index or instrument name for which you want to find the ITM strike prices (e.g., 'NIFTY', 'BANKNIFTY').
         - Expiry (int): The expiry to select.
            - 0 - Current week/month (depending on expiry type)
            - 1 - Next week/month (depending on expiry type)
            - and so on for subsequent weeks/months.
         - ITM_count (int): The number of steps to move away from the ATM strike to find the ITM strike prices (e.g., 1 means 1 step closer to the underlying price).
      
      - Returns:
         - CE_symbol_name (str): The option symbol for the ITM Call strike.
         - PE_symbol_name (str): The option symbol for the ITM Put strike.
         - CE_strike (int): The ITM Call strike price.
         - PE_strike (int): The ITM Put strike price.
      
      - Sample Code:         
         ```python      
            CE_symbol_name, PE_symbol_name, CE_strike, PE_strike = tsl.ITM_Strike_Selection(Underlying='NIFTY', Expiry=0, ITM_count=1)
         ```     

---



4. **Option Greeks**

   Fetch Greeks for a specific option:

   *Get Option Greek*

      - tsl.get_option_greek(strike: int, expiry: int, asset: str, interest_rate: float, flag: str, scrip_type: str)

      - Arguments:
         - strike (int): The strike price of the option.
         - expiry (int): The expiry to select. 
            - 0 - Current week/month (depending on expiry type).
            - 1 - Next week/month (depending on expiry type).
         - and so on for subsequent weeks/months.
         - asset (str): The underlying asset for the option (e.g., 'NIFTY').
         - interest_rate (float): The interest rate to be used in calculations (e.g., 10).
         - flag (str): The Greek value to fetch.
         - 'price' - Option price.
         - 'delta' - Delta value.
         - 'delta2' - Second-order delta.
         - 'theta' - Theta value.
         - 'rho' - Rho value.
         - 'vega' - Vega value.
         - 'gamma' - Gamma value.
         - 'all_val' - All Greeks values in a dictionary.
         - scrip_type (str): The option type ('CE' for Call options, 'PE' for Put options).

      - Returns:
         - Depending on the flag, it returns the requested Greek value or all Greek values in a dictionary.

      - Sample Code:         
         ```python      
            all_values = tsl.get_option_greek(strike=24400, expiry=0, asset='NIFTY', interest_rate=10, flag='all_val', scrip_type='CE')
         ``` 

---



5. **Order Placement and Management**

   Place, modify, or cancel orders:

   *Get Order Placement*

      - tsl.order_placement(tradingsymbol: str, exchange: str, quantity: int, price: int, trigger_price: int, 
         order_type: str, transaction_type: str, trade_type: str, disclosed_quantity=0, after_market_order=False, 
         validity='DAY', amo_time='OPEN', bo_profit_value=None, bo_stop_loss_value=None, should_slice=False) -> str
      - Arguments:
         - tradingsymbol (str): The trading symbol (e.g., 'NIFTY 21 NOV 23300 CALL').
         - exchange (str): The exchange (e.g., 'NFO', 'MCX', 'NSE').
         - quantity (int): The number of contracts to buy/sell.
         - price (int): The price at which to place the order.
         - trigger_price (int): The trigger price for stop orders.
         - order_type (str): Type of order ('MARKET', 'LIMIT', 'STOPLIMIT', 'STOPMARKET').
         - transaction_type (str): Type of transaction ('BUY' or 'SELL').
         - trade_type (str): Type of trade ('MIS', 'MARGIN', 'MTF',  'CO', 'BO', 'CNC').
         - disclosed_quantity (int, optional): Quantity disclosed to the market (default is 0).
         - after_market_order (bool, optional): Whether it is an after-market order (default is False).
         - validity (str, optional): Validity of the order ('DAY', 'IOC').
         - amo_time (str, optional): AMO time ('PRE_OPEN', 'OPEN', 'OPEN_30', 'OPEN_60') if after-market order.
         - bo_profit_value (float, optional): Profit value for BO orders (default is None).
         - bo_stop_loss_value (float, optional): Stop loss value for BO orders (default is None).
         - should_slice(bool, optional): When it exceeds freeze limit whether to slice the order or not
      - Returns:
         - str: The order ID if the order is placed successfully, or None if there was an error.

      - Sample Orders:
         ```python 
            orderid1 = tsl.order_placement('NIFTY 21 NOV 24400 CALL','NFO', 75, 0.05, 0, 'LIMIT', 'BUY', 'MIS')
            print(orderid1)
            orderid2 = tsl.order_placement('YESBANK','NSE', 1, 0, 0, 'MARKET', 'BUY', 'MIS')
            print(orderid2)

            orderid = tsl.order_placement('SENSEX 06 SEP 81900 PUT','BFO',10, 0, 0, 'MARKET', 'BUY', 'MIS')
            orderid = tsl.order_placement('ACC','NSE', 1, 0, 0, 'MARKET', 'BUY', 'MIS')
            orderid = tsl.order_placement('CRUEDOIL DEC FUT','MCX', 1, 4567, 0, 'LIMIT', 'BUY', 'CNC')
            orderid = tsl.order_placement('ACC','NSE', 1, 2674, 2670, 'STOPLIMIT', 'BUY', 'MIS')
            orderid = tsl.order_placement('ACC','NSE', 1, 0, 2670, 'STOPMARKET', 'BUY', 'MIS')
         ```

      - Sample Code:
         ```python 
            orderid = tsl.order_placement(tradingsymbol='NIFTY 19 DEC 23300 CALL', exchange='NFO', quantity=75, price=0.05, trigger_price=0,order_type='LIMIT', transaction_type='BUY', trade_type='MIS')
         ```



   *Get Order Modification*

      - tsl.modify_order(order_id, order_type, quantity, price=0, trigger_price=0, disclosed_quantity=0, validity='DAY', leg_name=None) -> str

      - Arguments:
         - order_id (str): The unique ID of the order to be modified.
         - order_type (str): Type of the order. Options include:
               - 'LIMIT': Limit order.
               - 'MARKET': Market order.
               - 'STOPLIMIT': Stop-loss limit order.
               - 'STOPMARKET': Stop-loss market order.
         - quantity (int): The updated quantity for the order.
         - price (float, optional): The updated price for the order (default is 0).
         - trigger_price (float, optional): The updated trigger price for the order (default is 0).
         - disclosed_quantity (int, optional): The quantity to disclose (default is 0).
         - validity (str, optional): Validity of the order. Options are:
               - 'DAY': Order remains valid for the trading day (default).
               - 'IOC': Immediate or cancel.
         - leg_name (str, optional): The specific leg to modify (used for bracket/CO orders). Options are:
               - 'ENTRY_LEG': Entry leg of the order.
               - 'TARGET_LEG': Target leg of the order.
               - 'STOP_LOSS_LEG': Stop-loss leg of the order.
               - If not applicable, leave as None.

      - Returns:
         - str: The modified order ID if the modification is successful.
         - Raises an exception if the modification fails.

      - Sample Code:
         ```python 
            orderid = '12241210603927'
            modified_order_id = tsl.modify_order(order_id=orderid,order_type="LIMIT",quantity=50,price=0.1,trigger_price=0)
         ```



   *Get Order Cancelation*

      - tsl.cancel_order(OrderID: str) -> None

      - Arguments:
         - OrderID (str): The unique ID of the order to be canceled.

      - Returns:
         - str: The status of the canceled order if successful (e.g., "Cancelled").
         - Raises an exception if the cancellation fails.

      - Sample Code:
         ```python 
            orderid = '12241210603927'
            order_status = tsl.cancel_order(OrderID=orderid)
         ```



   *Get All Intraday Order Cancelation and Intraday Position Close*
   
   - To cancell all the intraday open and trigger pending orders, square off all the positions 
      
      - tsl.cancel_all_orders()

      - Sample Code:
         ```python 
            order_details = tsl.cancel_all_orders()
         ```   



   *Place Iceberg Order*

      - tsl.order_placement(tradingsymbol: str, exchange: str, transaction_type: str, quantity: int, order_type: str, trade_type: str, price: float, trigger_price: float = 0, disclosed_quantity: int = 0, after_market_order: bool = False, validity: str = 'DAY', amo_time: str = 'OPEN', bo_profit_value: float = None, bo_stop_loss_Value: float = None ) -> str | list

      - Arguments:
         - tradingsymbol (str): The symbol for the instrument to trade.
         - exchange (str): The exchange where the order is placed (e.g., NSE, NFO, MCX).
         - transaction_type (str): "BUY" or "SELL".
         - quantity (int): Total quantity to be ordered.
         - order_type (str): Type of order ("LIMIT", "MARKET", "STOPLIMIT", "STOPMARKET").
         - trade_type (str): Type of trade ("MIS", "CNC", "CO", "BO", etc.).
         - price (float): Price for the order (used for LIMIT orders).
         - trigger_price (float): Trigger price for stop-loss orders (default is 0).
         - disclosed_quantity (int): Quantity to disclose (default is 0).
         - after_market_order (bool): If true, places the order as an after-market order.
         - validity (str): Validity of the order ("DAY", "IOC").
         - amo_time (str): Timing for after-market orders ("PRE_OPEN", "OPEN", etc.).
         - bo_profit_value (float): Profit target value for bracket orders (default is None).
         - bo_stop_loss_Value (float): Stop-loss value for bracket orders (default is None).

      - Returns:
         - str: A single order ID if the order is not sliced.
         - list: A list of order IDs if the order involves multiple slices.
         - None: Returns None if an exception occurs.


      - Sample Code:
         ```python 
            order_ids = tsl.order_placement(tradingsymbol="NIFTY 27 JAN 26000 CALL",exchange="NFO",transaction_type="BUY",quantity=1820,order_type="LIMIT",trade_type="MIS",price=21.05, should_slice = True)
         ```
   


   *Get Order Details*

   - Get detailed information about a specific order

      - tsl.get_order_detail(orderid:str)

      - Arguments:
         - orderid: The unique identifier of the order.
         - debug (str, optional): Set to "YES" to print debug information (default is "NO").

      - Returns:
         - Dictionary containing details of the order, such as price, quantity, status, etc.


      - Sample Code:
         ```python
            orderid = '12241210603927' 
            order_details = tsl.get_order_detail(orderid=orderid)
         ```


*Get Order Status* 

   - Get the current status of a specific order

      - tsl.get_order_status(orderid:str)
      
      - Arguments:
         - orderid: The unique identifier of the order.
         - debug (str, optional): Set to "YES" to print debug information (default is "NO").

      - Returns:
         - String representing the status of the order (e.g., 'Pending', 'Completed').

      - Sample Code:
         ```python
            orderid = '12241210603927' 
            order_status = tsl.get_order_status(orderid=orderid)  
         ```



  *Get Order Executed Price* 

   - Get the average traded price of an executed order

      - tsl.get_executed_price(orderid:str)

      - Arguments:
         - orderid: The unique identifier of the order.
         - debug (str, optional): Set to "YES" to print debug information (default is "NO").

      - Returns:
         - Integer representing the average price at which the order was executed.

      - Sample Code:
         ```python
            orderid = '12241210603927' 
            order_price = tsl.get_executed_price(orderid=orderid)
         ```



  *Get Order Exchange Time* 

   - Get the exchange timestamp for a specific order
      
      - order_time = tsl.get_exchange_time(orderid=orderid)
      
      - Arguments:
         - orderid: The unique identifier of the order.
         - debug (str, optional): Set to "YES" to print debug information (default is "NO").
      - Returns:
         - String with the timestamp of the order execution as recorded by the exchange.

      - Sample Code:
         ```python
            orderid = '12241210603927' 
            order_time = tsl.get_exchange_time(orderid=orderid)
         ```



#### Super Order Placement

Super Orders allow you to place an **Entry + Target + Stoploss** together (with optional trailing), and manage each leg.

#### Place Super Order

- **Method**
  - `tsl.place_super_order(tradingsymbol: str, exchange: str, transaction_type: str, quantity: int, order_type: str, trade_type: str, price: float = 0, target_price: float = 0, stop_loss_price: float = 0, trailing_jump: float = 0) -> str`

- **Arguments**
  - `tradingsymbol` (str): Trading symbol (e.g., `TRIDENT`)
  - `exchange` (str): Exchange (e.g., `NSE`, `NFO`, `MCX`)
  - `transaction_type` (str): `BUY` or `SELL`
  - `quantity` (int): Quantity to trade
  - `order_type` (str): `LIMIT` / `MARKET` *(as supported)*
  - `trade_type` (str): `MIS` / `CNC` / etc
  - `price` (float): Entry price (required for `LIMIT`)
  - `target_price` (float): Target price for target leg
  - `stop_loss_price` (float): Stoploss price for SL leg
  - `trailing_jump` (float): Trailing jump value (0 to disable)

- **Returns**
  - `str`: Super order ID if placed successfully, else `None` / error

- **Sample Code**
  ```python
  order_id = tsl.place_super_order(tradingsymbol="TRIDENT",exchange="NSE",transaction_type="BUY",quantity=1,order_type="LIMIT",trade_type="MIS",price=25,target_price=27,stop_loss_price=24,trailing_jump=0.2)
  print(order_id)
  ```

#### Modify Super Order

Use `leg_name` to modify a specific leg of the super order.

- **Method**
  - `tsl.modify_super_order(order_id: str, order_type: str, quantity: int, price: float = 0, target_price: float = 0, stop_loss_price: float = 0, trailing_jump: float = 0, leg_name: str = None) -> str`

- **Arguments**
  - `order_id` (str): Super order ID to be modified
  - `order_type` (str): `LIMIT` / `MARKET` *(as supported)*
  - `quantity` (int): Updated quantity
  - `price` (float, optional): Updated entry price (mainly for `ENTRY_LEG`)
  - `target_price` (float, optional): Updated target price (for `TARGET_LEG`)
  - `stop_loss_price` (float, optional): Updated stoploss price (for `STOP_LOSS_LEG`)
  - `trailing_jump` (float, optional): Updated trailing jump value
  - `leg_name` (str): Leg to modify:
    - `ENTRY_LEG`
    - `TARGET_LEG`
    - `STOP_LOSS_LEG`

- **Returns**
  - `str`: Modified order id / response id if successful

- **Sample Code**
  ```python
  modify_order_id = tsl.modify_super_order(order_id=order_id,order_type="LIMIT",quantity=1,price=24.9,target_price=26.9,stop_loss_price=23.9,trailing_jump=0.2,leg_name="ENTRY_LEG")
  print(modify_order_id)
  ```

#### Cancel Super Order

You can cancel a specific leg (Entry / Target / Stoploss) using `leg_name`.

- **Method**
  - `tsl.cancel_super_order(order_id: str, leg_name: str = None) -> str`

- **Arguments**
  - `order_id` (str): Super order ID to be cancelled
  - `leg_name` (str): Leg to cancel:
    - `ENTRY_LEG`
    - `TARGET_LEG`
    - `STOP_LOSS_LEG`

- **Returns**
  - `str`: Cancel status / cancel order id

- **Sample Code**
  ```python
  cancel_order_id = tsl.cancel_super_order(order_id=order_id,leg_name="ENTRY_LEG")
  print(cancel_order_id)
  ```

#### Fetch Super Orders

Fetch the details of all super orders.

- **Method**
  - `tsl.get_super_orders()`

- **Returns**
  - `list`: Super orders data

- **Sample Code**
  ```python
  super_orders = tsl.get_super_orders()
  print(super_orders)
  ```

---

### Forever Orders Placement

Forever Orders (GTT) let you place long-validity orders that trigger when price conditions are met.

Supported `order_flag` examples:
- `SINGLE` → Single trigger order
- `OCO` → One-Cancels-the-Other (2 legs)


#### Place Forever Order

- **Method**
  - `tsl.place_forever_order(tradingsymbol: str, exchange: str, transaction_type: str, quantity: int, order_type: str, trade_type: str, price: float = 0, trigger_price: float = 0, order_flag: str = "SINGLE", disclosed_quantity: int = 0, validity: str = "DAY", quantity_1: int = 0, price_1: float = 0, trigger_price_1: float = 0) -> str`

- **Sample Code (SINGLE)**
  ```python
  forever_order_id = tsl.place_forever_order( tradingsymbol="TRIDENT", exchange="NSE", transaction_type="BUY", quantity=1, order_type="LIMIT", trade_type="CNC", price=25, trigger_price=25.05, order_flag="SINGLE")
  ```

#### Modify Forever Order

- **Method**
  - `tsl.modify_forever_order(order_id: str, order_type: str, quantity: int, price: float = 0, trigger_price: float = 0, disclosed_quantity: int = 0, validity: str = "DAY", leg_name: str = None) -> str`

- **Arguments**
  - `order_id` (str): Super order ID to be modified
  - `order_type` (str): `LIMIT` / `MARKET` *(as supported)*
  - `quantity` (int): Updated quantity
  - `price` (float, optional): Updated entry price (mainly for `ENTRY_LEG`)
  - `target_price` (float, optional): Updated trigger price
    - `leg_name` (str): Leg to modify:
    - `ENTRY_LEG`
    - `TARGET_LEG`
    - `STOP_LOSS_LEG`

- **Returns**
  - `str`: Modified order id 

- **Sample Code**
  ```python
  modify_forever_order_id = tsl.modify_forever_order(order_id=forever_order_id, order_type="LIMIT", quantity=1, price=24.9, trigger_price=24.7, disclosed_quantity=0, validity="DAY", leg_name="STOP_LOSS_LEG", order_flag="SINGLE")
  ```

#### Cancel Super Order

- **Method**
  - `tsl.cancel_forever_order(order_id: str) -> str`

- **Returns**
  - `str`: cancel order id

- **Sample Code**
  ```python
  cancel_order_id = tsl.cancel_forever_order(order_id=order_id)
  print(cancel_order_id)
  ```

#### Fetch Forever Orders

Fetch the details of all forever orders.

- **Method**
  - `tsl.get_forever_orders()`

- **Returns**
  - `list`: Forever orders data

- **Sample Code**
  ```python
  forever_orders = tsl.get_forever_orders()
  print(forever_orders)
  ```

---
6. **Portfolio Management**

   Fetch holdings, positions, and balances:

   *Get Holdings*

   - Fetch current holdings
      
      - tsl.get_holdings(debug="NO") 

      - Arguments:
         - debug (str, optional): Set to "YES" to print debug information (default is "NO").
      
      - Returns:
         - pd.DataFrame: A DataFrame containing the list of holdings, including details like symbol, quantity, and average price.
         - In case of an error, returns a dictionary with 'status' as 'failure', error message, and data.

      - Sample Code:
         ```python 
            holdings = tsl.get_holdings()
         ```



   *Get Positions*

   - Fetch current open positions

      - tsl.get_positions(debug="NO")
      - Arguments:
         - debug (str, optional): Set to "YES" to print debug information (default is "NO").

      - Returns:
         - pd.DataFrame: A DataFrame containing the list of open positions with details like symbol, quantity, average price, etc.
         - In case of an error, returns a dictionary with 'status' as 'failure', error message, and data.

         - Sample Code:
            ```python 
               positions = tsl.get_positions()
            ```



   *Get Orderbook*
   
   - Fetch the order book

      - tsl.get_orderbook(debug="NO")
         
      - Arguments:
         - debug (str, optional): Set to "YES" to print debug information (default is "NO").

      - Returns:
         - pd.DataFrame: A DataFrame containing the list of all orders placed, including details such as symbol, quantity, status, and price.
         - In case of an error, returns a dictionary with 'status' as 'failure', error message, and data.

      - Sample Code:
         ```python 
            orderbook = tsl.get_orderbook()
         ```   



   *Get Tradebook*

   - Fetch the trade book

      - tsl.get_trade_book(debug="NO")

      - Arguments:
         - debug (str, optional): Set to "YES" to print debug information (default is "NO").

      - Returns:
         - pd.DataFrame: A DataFrame containing the list of all completed trades with details such as symbol, quantity, price, and trade time.
         - In case of an error, returns a dictionary with 'status' as 'failure', error message, and data.   

      - Sample Code:
         ```python 
            tradebook = tsl.get_trade_book()
         ```         



   *Get Balance*
   
   - To get the available balance from the Dhan API client
      
      - tsl.get_balance()
      
      - Sample Code:
         ```python    
            available_balance = tsl.get_balance()
         ``` 



   *Get Live PNL*

   - To get the live PNL of current positions
      
      - tsl.get_live_pnl()
      
      - Sample Code:
         ```python    
            PNL = tsl.get_live_pnl()
         ```    



   *Get Lot Size*

   - To get the lot size for the futures and options
      
      - tsl.get_lot_size(Tradingsymbol: str)
      
      - Sample Code:
         ```python    
            lot_size = tsl.get_lot_size(tradingsymbol = 'NIFTY 19 DEC 24400 CALL')
         ```      



   *Get Margin for Tradingsymbol*

   - To get the margin for the stocks, futures and options
      
      - tsl.margin_calculator(tradingsymbol: str, exchange: str, transaction_type: str, quantity: int, trade_type: str, price: float, trigger_price:float)
      
      - Sample Code:
         ```python    
            Margin = tsl.margin_calculator(tradingsymbol='NIFTY DEC FUT', exchange='NFO', transaction_type='BUY', quantity=75, trade_type='MARGIN', price=24350, trigger_price=0)
         ```     

---



7. **Option Chain Analysis**

   Retrieve and analyze the option chain:

   *Get Option Chain*

      - tsl.get_option_chain(Underlying: str, exchange: str, expiry: int, num_strikes: int = 10) -> pd.DataFrame | None

      - Arguments:
         - Underlying (str): The symbol of the underlying asset (e.g., "NIFTY", "BANKNIFTY", "RELIANCE").
         - exchange (str): The exchange where the options are traded (e.g., "NSE", "NFO", "MCX").
         - expiry (int): Index of the expiry date in the list of available expiry dates (0 for the nearest expiry).
         - num_strikes (int, optional): Number of strikes to include in the option chain (default is 10).

      - Returns:
         - pd.DataFrame: A formatted DataFrame containing the option chain data with details like strike price, call/put LTP, OI, volume, etc.
         - None: Returns None if there is an error or no expiry data is found.

      - Sample Code:         
         ```python      
            option_chain = tsl.get_option_chain(Underlying="NIFTY", exchange="INDEX", expiry=0, num_strikes=10)
         ``` 

---

8. **Fetch Expired Option Chart Data**

   Retrieve minute-wise OHLC, Volume, IV, OI, Spot, and Strike data for expired option contracts (index options only, as supported by DHAN).

   *Get Expired Option Data*

      - tsl.get_expired_option_data(tradingsymbol: str,exchange: str,interval: int,expiry_flag: str,expiry_code: int,strike: str = "ATM",option_type: str = "CALL",required_data: list = None,from_date: str = "",to_date: str = "")


      - Arguments:
         - tradingsymbol (str): The symbol for which historical expired option data is required  
            (e.g., `"NIFTY"`, `"BANKNIFTY"`, `"RELIANCE"`).
         - exchange (str): Exchange of the underlying  
            Allowed: `"NSE"`, `"BSE"`
         - interval (int): Candle interval in minutes  
            Allowed: `1`, `5`, `15`, `25`, `60`.
         - expiry_flag (str): The expiry type  
            - `"MONTH"` for monthly contracts  
            - `"WEEK"` for weekly contracts
         - expiry_code (int): Expiry sequence number  
            - `1` → Near expiry  
            - `2` → Next expiry  
            - `3` → Far expiry
         - strike (str): Strike selection mode  
            Examples: `"ATM"`, `"ATM+3"`, `"ATM-3"`.
         - option_type (str): `"CALL"` or `"PUT"`.
         - required_data (list, optional): Which fields to fetch  
            Default: `["open","high","low","close","volume","iv","oi","spot","strike"]`
         - from_date (str): Start date in `YYYY-MM-DD` format.
         - to_date (str): End date in `YYYY-MM-DD` format.

   - Sample Code:
      ```python
      data = tsl.get_expired_option_data(tradingsymbol="RELIANCE",exchange="NSE",interval=1,expiry_flag="MONTH",expiry_code=1,strike="ATM",option_type="CALL",from_date="2024-10-10",to_date="2024-11-10")
      ```
---

9. **Full Market Depth Data**

   Retrieve live 20-level bid/ask orderbook depth for NSE and BSE instruments

   *Get Market Depth Data*
   
      - tsl.full_market_depth_data(symbols)

         - Arguments:
            - symbols with exchanges(tuple or list of tuples): Instrument(s) for which you want full market depth
               - Single symbol example:
                  - ("RELIANCE", "NSE")
               - Multiple symbols example:
                  - [
                        ("RELIANCE", "NSE"),
                        ("SENSEX 11 DEC 85800 CALL", "BFO"),
                        ("NIFTY 09 DEC 26000 CALL", "NFO"),
                        ("NIFTY 09 DEC 26000 PUT", "NFO"),
                    ]

         - Returns:
            - For a single symbol:
               - A single depth client object (to be passed to get_market_depth_df)
            - For multiple symbols:
               - A dictionary in the format:
                 - "RELIANCE|NSE" → <depth_client>
                 - "NIFTY 09 DEC 26000 CALL|NFO" → <depth_client>

   *Parse Market Depth into DataFrames*
   
      - tsl.get_market_depth_df(depth_client)

         - Returns:
            - bid_df: Bid side DataFrame
            - ask_df: Ask side DataFrame

         - Columns in DataFrames:
            - level - depth level
            - bid_price, bid_qty, bid_orders
            - ask_price, ask_qty, ask_orders

   *Sample Code*
   
   ```python
   # Single Symbol
   depth_client = tsl.full_market_depth_data(("RELIANCE", "NSE"))

   for key, depth_client in depth_data.items():
      bid_df, ask_df = tsl.get_market_depth_df(depth_client)
   ```

   ```python
   # Multiple Symbols
   symbol_list = [
    ("RELIANCE", "NSE"),
    ("SENSEX 11 DEC 85800 CALL", "BFO"),
    ("NIFTY 09 DEC 26000 CALL", "NFO"),
    ("NIFTY 09 DEC 26000 PUT", "NFO")]
   depth_data = tsl.full_market_depth_data(symbol_list)

   for key, depth_client in depth_data.items():
      bid_df, ask_df = tsl.get_market_depth_df(depth_client)
   ```

---

10. **Alerts via Telegram**

   send a Alerts via Telegram

      *Send Telegram Alerts*

      - tsl.send_telegram_alert(message: str,receiver_chat_id: str,bot_token: str) -> None

      - Arguments:
         - message (str): The text message to send. Supports basic text formatting.
         - receiver_chat_id (str): The unique chat ID of the Telegram user or group. 
               - For individual users: Use their chat ID.
               - For groups: Use the group’s chat ID (ensure the bot is added to the group).
         - bot_token (str): The authorization token of the Telegram bot. 
               - Obtainable when creating a bot via the Telegram BotFather.

      - Returns:
         - None: The function prints a success or failure message in the console.   

      - Sample Code:         
         ```python      
            tsl.send_telegram_alert(message="Order executed: BUY 50 shares of RELIANCE",receiver_chat_id="123456789",bot_token="123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZ")
         ``` 

---


### Notes
Ensure your token_id is valid for the session. Tokens expire after a set period.
Always verify the data and status of API responses before processing.
For debugging, use Python's pdb or enable debug mode in API calls by setting debug="YES".


### License
This project is licensed under the MIT License. See the LICENSE file for details.

### Contact
For queries or issues, please contact: contact.tradehull@gmail.com.

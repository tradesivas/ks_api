#----------------------- Import section ---------------------
from ks_api_client import ks_api
import os
from dotenv import load_dotenv
import pandas as pd
from tkinter import *
#------------------------ Get Env Section ---------------------
load_dotenv()
access_token = os.getenv("access_token")
userid = os.getenv("userid")
consumer_key = os.getenv("consumer_key")
password = os.getenv("password")
host = os.getenv("host")
otp = os.getenv("otp")
expiry = os.getenv("expiry")
instrumentName = 'FINNIFTY'
optionType = 'CE'
#------------------------ Loading ScripMaster File ----------------
df = pd.read_csv ("TradeApiInstruments_FNO_06_01_2023.txt",sep="|")
#------------------------ Login Credential Section ----------------
client = ks_api.KSTradeApi(access_token = access_token, userid = userid, \
                consumer_key = consumer_key, ip = "127.0.0.1", app_id = "", host = host)
#------------------------ Place Order functions --------------------
isbuyinstrument = 0
issellinstrument= 0
def buy_instrument():
    global isbuyinstrument
    global issellinstrument
    if isbuyinstrument == 0 and issellinstrument== 0:
        client.place_order(order_type = "N", instrument_token = instrumentToken, transaction_type = "BUY",\
                   quantity = 40, price = 0, disclosed_quantity = 0, trigger_price = 0,\
                   tag = "python Button buyif 1", validity = "GFD", variety = "REGULAR")
        print('Buy order placed for instrument')
        isbuyinstrument+= 1
    elif issellinstrument== 1 and isbuyinstrument ==0:
        client.place_order(order_type = "N", instrument_token = instrumentToken, transaction_type = "BUY",\
                   quantity = 40, price = 0, disclosed_quantity = 0, trigger_price = 0,\
                   tag = "python Button buyif 2", validity = "GFD", variety = "REGULAR")
        print('sell order closed for instrument')
        isbuyinstrument = 0
        issellinstrument= 0
    else:
        print('instrument already bought')
def sell_instrument():
    global isbuyinstrument
    global issellinstrument
    if issellinstrument== 0 and isbuyinstrument == 0:
        client.place_order(order_type = "N", instrument_token = instrumentToken, transaction_type = "SELL",\
                   quantity = 1, price = 0, disclosed_quantity = 0, trigger_price = 0,\
                   tag = "python Button sellif 1", validity = "GFD", variety = "REGULAR")
        print('Sell order placed for instrument')
        issellinstrument+= 1
    elif isbuyinstrument == 1 and issellinstrument==0:
        client.place_order(order_type = "N", instrument_token = instrumentToken, transaction_type = "SELL",\
                   quantity = 1, price = 0, disclosed_quantity = 0, trigger_price = 0,\
                   tag = "python Button sellif 2", validity = "GFD", variety = "REGULAR")
        print('Buy order closed for instrument')
        isbuyinstrument = 0
        issellinstrument= 0
    else:
        print('instrument already sold')
































#------------------------ Get session for user --------------------
login_response = client.login(password = password)
print("---------------login response---------------")
print(login_response)
#Generated session token
session_response = client.session_2fa(access_code = otp)
print("---------------session response---------------")
print(session_response)
#buy_strike = float(input("Enter Buy Strike: "))
quote_response = client.quote(instrument_token = 11721)
print(quote_response)
ltp = quote_response['success'][0]['ltp']
ltp=float(ltp)
print(ltp)
atm = round(ltp/50)*50
print(atm)
instrumentToken = df.loc[(df['instrumentName'] == 'NIFTY') & (df['expiry'] == '12JAN23') & (df['optionType'] == 'CE') & (df['strike'] == atm), 'instrumentToken'].iloc[0]
instrumentToken = int(instrumentToken)
# quote_response = client.quote(instrument_token = instrumentToken)
# print(quote_response)
# ltp = quote_response['success'][0]['ltp']
# ltp=float(ltp)
# print(ltp)
# client.place_order(order_type = "N", instrument_token = instrumentToken, transaction_type = "BUY",\
#                    quantity = 1, price = 0, disclosed_quantity = 0, trigger_price = 0,\
#                    tag = "Order_By_Python_b_c_d_bnf_py", validity = "GFD", variety = "REGULAR")


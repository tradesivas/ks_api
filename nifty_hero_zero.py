#                           ________________________________________________________________
#                           |                Before run the code                            |
#                           |---------------------------------------------------------------|
#                           |   1. download Scripmaster using down_ks_Scripmaster.py        |
#                           |   2. change nifty expiry to current expiry in .env file       |
#                           |   3. enter latest otp in .env file                            |   
#                           |   4. change date in TradeApiInstruments_FNO_10_01_2023.txt    |
#                           |       in this code                                            |
#                           |_______________________________________________________________|

from tkinter import *
from asyncio.windows_events import NULL
import ks_api_client
from ks_api_client import ks_api
import os
from dotenv import load_dotenv
import pandas as pd
import time
df = pd.read_csv ("TradeApiInstruments_FNO_10_01_2023.txt",sep="|") #change needed every day
load_dotenv()
access_token = os.getenv("access_token")
userid = os.getenv("userid")
consumer_key = os.getenv("consumer_key")
password = os.getenv("password")
host = os.getenv("host")
otp = os.getenv("otp")
expiry = os.getenv("nifty_expiry")
instrumentName = 'NIFTY'
underlying_token = 11721

client = ks_api.KSTradeApi(access_token = access_token, userid = userid, \
                consumer_key = consumer_key, ip = "127.0.0.1", app_id = "", host = host)
isbuyniftyce = 0
isbuyniftype = 0
def buy_niftyce():
    global isbuyniftyce
    global ceinstrumentToken
    if isbuyniftyce == 0:
        client.login(password = password)
        client.session_2fa(access_code = otp)
        quote_response = client.quote(instrument_token = 35881)
        ltp = quote_response['success'][0]['ltp']
        ltp = float(ltp)
        atm = round(ltp/50)*50
        print(atm)
        ceinstrumentToken = df.loc[(df['instrumentName'] == 'FINNIFTY') & (df['expiry'] == expiry) & (df['optionType'] == 'CE') & (df['strike'] == atm), 'instrumentToken'].iloc[0]
        ceinstrumentToken  = int(ceinstrumentToken)
        order_response = client.place_order(order_type = "N", instrument_token = ceinstrumentToken, transaction_type = "BUY",\
                   quantity = 40, price = 0, disclosed_quantity = 0, trigger_price = 0,\
                   tag = "python Button buyif 1", validity = "GFD", variety = "REGULAR")
        print("Buy order placed for FINNIFTY Option CE")
        print(order_response)
        o_id = order_response['Success']['NSE']['orderId']
        print("OrderId= ",o_id)
        netq = 99999
        status = 'OPN'
        while ((netq != 0) or (netq == 40)) and status == 'OPN':
            o_r=client.order_report(order_id = o_id)
            print(o_r)
            l1 = len(o_r['success'])
            print("Lenth = ",l1)
            netq = (o_r['success'][(l1-1)]['orderQuantity']) - (o_r['success'][(l1-1)]['filledQuantity'])
            print(netq)
            status = (o_r['success'][(l1-1)]['status'])
            time.sleep(1)
        isbuyniftyce+= 1
        print("Buy CE Order Filled")
    
def sell_niftyce():
    global isbuyniftyce
    global ceinstrumentToken
    if isbuyniftyce == 1:
        order_response = client.place_order(order_type = "N", instrument_token = ceinstrumentToken, transaction_type = "SELL",\
                   quantity = 40, price = 0, disclosed_quantity = 0, trigger_price = 0,\
                   tag = "python Button sellif 1", validity = "GFD", variety = "REGULAR")
        print('Sell order placed for FINNIFTY Option CE')
    else:
        print('No CE option to Sell')

def buy_niftype():
    global isbuyniftype
    global peinstrumentToken
    if isbuyniftype == 0:
        client.login(password = password)
        client.session_2fa(access_code = otp)
        quote_response = client.quote(instrument_token = 35881)
        ltp = quote_response['success'][0]['ltp']
        ltp = float(ltp)
        atm = round(ltp/50)*50
        print(atm)
        peinstrumentToken = df.loc[(df['instrumentName'] == 'FINNIFTY') & (df['expiry'] == expiry) & (df['optionType'] == 'PE') & (df['strike'] == atm), 'instrumentToken'].iloc[0]
        peinstrumentToken  = int(peinstrumentToken)
        order_response = client.place_order(order_type = "N", instrument_token = peinstrumentToken, transaction_type = "BUY",\
                   quantity = 40, price = 0, disclosed_quantity = 0, trigger_price = 0,\
                   tag = "python Button buyif 1", validity = "GFD", variety = "REGULAR")
        print("Buy order placed for FINNIFTY Option PE")
        print(order_response)
        o_id = order_response['Success']['NSE']['orderId']
        print("OrderId= ",o_id)
        netq = 99999
        status = 'OPN'
        while ((netq != 0) or (netq == 40)) and status == 'OPN':
            o_r=client.order_report(order_id = o_id)
            print(o_r)
            l1 = len(o_r['success'])
            print("Lenth = ",l1)
            netq = (o_r['success'][(l1-1)]['orderQuantity']) - (o_r['success'][(l1-1)]['filledQuantity'])
            print(netq)
            status = (o_r['success'][(l1-1)]['status'])
            time.sleep(1)
        isbuyniftype+= 1
        print("Buy PE Order Filled")
    
def sell_niftype():
    global isbuyniftype
    global peinstrumentToken
    if isbuyniftype == 1:
        order_response = client.place_order(order_type = "N", instrument_token = peinstrumentToken, transaction_type = "SELL",\
                   quantity = 40, price = 0, disclosed_quantity = 0, trigger_price = 0,\
                   tag = "python Button sellif 1", validity = "GFD", variety = "REGULAR")
        print('Sell order placed for FINNIFTY Option PE')
    else:
        print('No PE option to Sell')

root = Tk()
frame = Frame(root)
frame.pack()
bottomframe = Frame(root)
bottomframe.pack( side = BOTTOM )
buy_niftyce_button = Button(frame, text = 'FINNIFTY CE'+'\n\n'+'1', bg = 'green', fg ='black',height = 5, width = 15, command=buy_niftyce)
buy_niftyce_button.pack( side = LEFT)
sell_niftyce_button = Button(frame, text = 'FINNIFTY CE'+'\n\n'+'1', bg = 'red', fg ='black',height = 5, width = 15, command=sell_niftyce)
sell_niftyce_button.pack( side = LEFT)
buy_niftype_button = Button(bottomframe, text = 'FINNIFTY PE'+'\n\n'+'1', bg = 'green', fg ='black',height = 5, width = 15, command=buy_niftype)
buy_niftype_button.pack( side = LEFT)
sell_niftype_button = Button(bottomframe, text = 'FINNIFTY PE'+'\n\n'+'1', bg = 'red', fg ='black',height = 5, width = 15, command=sell_niftype)
sell_niftype_button.pack( side = LEFT)
root.attributes('-topmost',True)
root.mainloop()
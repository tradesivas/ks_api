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
df = pd.read_csv ("ks_fno_scripmaster.txt",sep="|") #change needed every day
load_dotenv()
access_token = os.getenv("access_token")
userid = os.getenv("userid")
consumer_key = os.getenv("consumer_key")
password = os.getenv("password")
host = os.getenv("host")
otp = os.getenv("otp")
expiry = os.getenv("banknifty_expiry")
instrumentName = 'BANKNIFTY'
underlying_token = 11717

client = ks_api.KSTradeApi(access_token = access_token, userid = userid, \
                consumer_key = consumer_key, ip = "127.0.0.1", app_id = "", host = host)
isbuybankniftyce = 0
isbuybankniftype = 0
def buy_bankniftyce():
    global isbuybankniftyce
    global ceinstrumentToken
    if isbuybankniftyce == 0:
        client.login(password = password)
        client.session_2fa(access_code = otp)
        quote_response = client.quote(instrument_token = underlying_token)
        ltp = quote_response['success'][0]['ltp']
        ltp = float(ltp)
        atm = round(ltp/100)*100
        print(atm)
        ceinstrumentToken = df.loc[(df['instrumentName'] == 'BANKNIFTY') & (df['expiry'] == expiry) & (df['optionType'] == 'CE') & (df['strike'] == atm), 'instrumentToken'].iloc[0]
        ceinstrumentToken  = int(ceinstrumentToken)
        order_response = client.place_order(order_type = "N", instrument_token = ceinstrumentToken, transaction_type = "BUY",\
                   quantity = 25, price = 0, disclosed_quantity = 0, trigger_price = 0,\
                   tag = "python Button buyif 1", validity = "GFD", variety = "REGULAR")
        print("Buy order placed for BANKNIFTY Option CE")
        print(order_response)
        o_id = order_response['Success']['NSE']['orderId']
        print("OrderId= ",o_id)
        netq = 99999
        status = 'OPN'
        while ((netq != 0) or (netq == 25)) and status == 'OPN':
            o_r=client.order_report(order_id = o_id)
            print(o_r)
            l1 = len(o_r['success'])
            print("Lenth = ",l1)
            netq = (o_r['success'][(l1-1)]['orderQuantity']) - (o_r['success'][(l1-1)]['filledQuantity'])
            print(netq)
            status = (o_r['success'][(l1-1)]['status'])
            time.sleep(1)
        isbuybankniftyce+= 1
        print("Buy BANKNIFTY CE Order Filled")
    
def sell_bankniftyce():
    global isbuybankniftyce
    global ceinstrumentToken
    if isbuybankniftyce == 1:
        order_response = client.place_order(order_type = "N", instrument_token = ceinstrumentToken, transaction_type = "SELL",\
                   quantity = 25, price = 0, disclosed_quantity = 0, trigger_price = 0,\
                   tag = "python Button sellif 1", validity = "GFD", variety = "REGULAR")
        print('Sell order placed for BANKNIFTY Option CE')
        isbuybankniftyce-= 1
    else:
        print('No BANKNIFTY CE option to Sell')

def buy_bankniftype():
    global isbuybankniftype
    global peinstrumentToken
    if isbuybankniftype == 0:
        client.login(password = password)
        client.session_2fa(access_code = otp)
        quote_response = client.quote(instrument_token = underlying_token)
        ltp = quote_response['success'][0]['ltp']
        ltp = float(ltp)
        atm = round(ltp/100)*100
        print(atm)
        peinstrumentToken = df.loc[(df['instrumentName'] == 'BANKNIFTY') & (df['expiry'] == expiry) & (df['optionType'] == 'PE') & (df['strike'] == atm), 'instrumentToken'].iloc[0]
        peinstrumentToken  = int(peinstrumentToken)
        order_response = client.place_order(order_type = "N", instrument_token = peinstrumentToken, transaction_type = "BUY",\
                   quantity = 25, price = 0, disclosed_quantity = 0, trigger_price = 0,\
                   tag = "python Button buyif 1", validity = "GFD", variety = "REGULAR")
        print("Buy order placed for BANKNIFTY Option PE")
        print(order_response)
        o_id = order_response['Success']['NSE']['orderId']
        print("OrderId= ",o_id)
        netq = 99999
        status = 'OPN'
        while ((netq != 0) or (netq == 25)) and status == 'OPN':
            o_r=client.order_report(order_id = o_id)
            print(o_r)
            l1 = len(o_r['success'])
            print("Lenth = ",l1)
            netq = (o_r['success'][(l1-1)]['orderQuantity']) - (o_r['success'][(l1-1)]['filledQuantity'])
            print(netq)
            status = (o_r['success'][(l1-1)]['status'])
            time.sleep(1)
        isbuybankniftype+= 1
        print("Buy BANKNIFTY PE Order Filled")
    
def sell_bankniftype():
    global isbuybankniftype
    global peinstrumentToken
    if isbuybankniftype == 1:
        order_response = client.place_order(order_type = "N", instrument_token = peinstrumentToken, transaction_type = "SELL",\
                   quantity = 25, price = 0, disclosed_quantity = 0, trigger_price = 0,\
                   tag = "python Button sellif 1", validity = "GFD", variety = "REGULAR")
        print('Sell order placed for BANKNIFTY Option PE')
        isbuybankniftype-= 1
    else:
        print('No BANKNIFTY PE option to Sell')

bnfroot = Tk()
frame = Frame(bnfroot)
frame.pack()
bottomframe = Frame(bnfroot)
bottomframe.pack( side = BOTTOM )
buy_bankniftyce_button = Button(frame, text = 'BANKNIFTY CE'+'\n\n'+'1', bg = 'green', fg ='black',height = 5, width = 15, command=buy_bankniftyce)
buy_bankniftyce_button.pack( side = LEFT)
sell_bankniftyce_button = Button(frame, text = 'BANKNIFTY CE'+'\n\n'+'1', bg = 'red', fg ='black',height = 5, width = 15, command=sell_bankniftyce)
sell_bankniftyce_button.pack( side = LEFT)
buy_bankniftype_button = Button(bottomframe, text = 'BANKNIFTY PE'+'\n\n'+'1', bg = 'green', fg ='black',height = 5, width = 15, command=buy_bankniftype)
buy_bankniftype_button.pack( side = LEFT)
sell_bankniftype_button = Button(bottomframe, text = 'BANKNIFTY PE'+'\n\n'+'1', bg = 'red', fg ='black',height = 5, width = 15, command=sell_bankniftype)
sell_bankniftype_button.pack( side = LEFT)
bnfroot.attributes('-topmost',True)
bnfroot.mainloop()
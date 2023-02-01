#                           ________________________________________________________________
#                           |                Before run the code                            |
#                           |---------------------------------------------------------------|
#                           |   1. download Scripmaster using down_ks_Scripmaster.py        |
#                           |   2. change finnifty expiry to current expiry in .env file    |
#                           |   3. enter latest otp in .env file                            |   
#                           |                                             |
#                           |_______________________________________________________________|

from tkinter import *
from ks_api_client import ks_api
import os
from dotenv import load_dotenv
import pandas as pd
import time

load_dotenv()
access_token = os.getenv("access_token")
userid = os.getenv("userid")
consumer_key = os.getenv("consumer_key")
password = os.getenv("password")
host = os.getenv("host")
otp = os.getenv("otp")
expiry = os.getenv("finnifty_expiry")
instrumentName = 'FINNIFTY'

df = pd.read_csv ("ks_fno_scripmaster.txt",sep="|")
client = ks_api.KSTradeApi(access_token = access_token, userid = userid, \
                consumer_key = consumer_key, ip = "127.0.0.1", app_id = "", host = host)
issellfince = 0
issellfinpe = 0
def sell_fince():
    global issellfince
    global ceinstrumentToken
    if issellfince == 0:
        client.login(password = password)
        client.session_2fa(access_code = otp)
        quote_response = client.quote(instrument_token = 35881)
        ltp = quote_response['success'][0]['ltp']
        ltp = float(ltp)
        atm = round(ltp/50)*50
        print(atm)
        ceinstrumentToken = df.loc[(df['instrumentName'] == 'FINNIFTY') & (df['expiry'] == expiry) & (df['optionType'] == 'CE') & (df['strike'] == atm), 'instrumentToken'].iloc[0]
        ceinstrumentToken  = int(ceinstrumentToken)
        order_response = client.place_order(order_type = "N", instrument_token = ceinstrumentToken, transaction_type = "SELL",\
                   quantity = 40, price = 0, disclosed_quantity = 0, trigger_price = 0,\
                   tag = "python Button Sellif 1", validity = "GFD", variety = "REGULAR")
        print("Sell order placed for FINNIFTY Option CE")
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
        issellfince+= 1
        print("Sell CE Order Filled")
        
    
def buy_fince():
    global issellfince
    global ceinstrumentToken
    if issellfince == 1:
        order_response = client.place_order(order_type = "N", instrument_token = ceinstrumentToken, transaction_type = "BUY",\
                   quantity = 40, price = 0, disclosed_quantity = 0, trigger_price = 0,\
                   tag = "python Button Buyif 1", validity = "GFD", variety = "REGULAR")
        print('exit Buy order placed for FINNIFTY Option CE')
    else:
        print('No CE option to sold to exit buy')

def sell_finpe():
    global issellfinpe
    global peinstrumentToken
    if issellfinpe == 0:
        client.login(password = password)
        client.session_2fa(access_code = otp)
        quote_response = client.quote(instrument_token = 35881)
        ltp = quote_response['success'][0]['ltp']
        ltp = float(ltp)
        atm = round(ltp/50)*50
        print(atm)
        peinstrumentToken = df.loc[(df['instrumentName'] == 'FINNIFTY') & (df['expiry'] == expiry) & (df['optionType'] == 'PE') & (df['strike'] == atm), 'instrumentToken'].iloc[0]
        peinstrumentToken  = int(peinstrumentToken)
        order_response = client.place_order(order_type = "N", instrument_token = peinstrumentToken, transaction_type = "SELL",\
                   quantity = 40, price = 0, disclosed_quantity = 0, trigger_price = 0,\
                   tag = "python Button Sellif 1", validity = "GFD", variety = "REGULAR")
        print("Sell order placed for FINNIFTY Option PE")
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
        issellfinpe+= 1
        print("Sell PE Order Filled")
    
def buy_finpe():
    global issellfinpe
    global peinstrumentToken
    if issellfinpe == 1:
        order_response = client.place_order(order_type = "N", instrument_token = peinstrumentToken, transaction_type = "BUY",\
                   quantity = 40, price = 0, disclosed_quantity = 0, trigger_price = 0,\
                   tag = "python Button Buyif 1", validity = "GFD", variety = "REGULAR")
        print('exit Buy order placed for FINNIFTY Option PE')
    else:
        print('No PE option sold to Exit Buy')

finroot = Tk()
frame = Frame(finroot)
frame.pack()
bottomframe = Frame(finroot)
bottomframe.pack( side = BOTTOM )
buy_fince_button = Button(frame, text = 'FINNIFTY CE'+'\n\n'+'1', bg = 'blue', fg ='black',height = 5, width = 15, command=buy_fince)
buy_fince_button.pack( side = LEFT)
sell_fince_button = Button(frame, text = 'FINNIFTY CE'+'\n\n'+'1', bg = 'red', fg ='black',height = 5, width = 15, command=sell_fince)
sell_fince_button.pack( side = LEFT)
buy_finpe_button = Button(bottomframe, text = 'FINNIFTY PE'+'\n\n'+'1', bg = 'blue', fg ='black',height = 5, width = 15, command=buy_finpe)
buy_finpe_button.pack( side = LEFT)
sell_finpe_button = Button(bottomframe, text = 'FINNIFTY PE'+'\n\n'+'1', bg = 'red', fg ='black',height = 5, width = 15, command=sell_finpe)
sell_finpe_button.pack( side = LEFT)
finroot.attributes('-topmost',True)
finroot.mainloop()
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
expiry = os.getenv("nifty_expiry")
instrumentName = 'NIFTY'
underlying_token = 11721

client = ks_api.KSTradeApi(access_token = access_token, userid = userid, \
                consumer_key = consumer_key, ip = "127.0.0.1", app_id = "", host = host)
isbuyniftyceatm = 0
issellniftyceotm = 0
iscespreadfilled = False
isbuyniftypeatm = 0
isselniftypeotm = 0
def buy_niftyce():
    global isbuyniftyceatm
    global issellniftyceotm
    global iscespreadfilled
    global atmceinstrumentToken
    global otmceinstrumentToken
    if isbuyniftyceatm == 0:
        client.login(password = password)
        client.session_2fa(access_code = otp)
        quote_response = client.quote(instrument_token = underlying_token)
        ltp = quote_response['success'][0]['ltp']
        ltp = float(ltp)
        atm = round(ltp/50)*50
        print(atm)
        atmceinstrumentToken = df.loc[(df['instrumentName'] == 'NIFTY') & (df['expiry'] == expiry) & (df['optionType'] == 'CE') & (df['strike'] == atm), 'instrumentToken'].iloc[0]
        atmceinstrumentToken  = int(atmceinstrumentToken)
        otmceinstrumentToken = atmceinstrumentToken + 50
        order_response = client.place_order(order_type = "N", instrument_token = atmceinstrumentToken, transaction_type = "BUY",\
                   quantity = 50, price = 0, disclosed_quantity = 0, trigger_price = 0,\
                   tag = "python Button buyif 1", validity = "GFD", variety = "REGULAR")
        print("Buy order placed for NIFTY Option CE")
        print(order_response)
        o_id = order_response['Success']['NSE']['orderId']
        print("OrderId= ",o_id)
        netq = 99999
        status = 'OPN'
        while ((netq != 0) or (netq == 50)) and status == 'OPN':
            o_r=client.order_report(order_id = o_id)
            print(o_r)
            l1 = len(o_r['success'])
            print("Lenth = ",l1)
            netq = (o_r['success'][(l1-1)]['orderQuantity']) - (o_r['success'][(l1-1)]['filledQuantity'])
            print(netq)
            status = (o_r['success'][(l1-1)]['status'])
            time.sleep(1)
        isbuyniftyceatm+= 1
        print("BUY NIFTY CE Order Filled")
        if isbuyniftyceatm == 1:
            order_response = client.place_order(order_type = "N", instrument_token = otmceinstrumentToken, transaction_type = "SELL",\
                    quantity = 50, price = 0, disclosed_quantity = 0, trigger_price = 0,\
                    tag = "python Button buyif 1", validity = "GFD", variety = "REGULAR")
            print("SELL order placed for NIFTY Option CE")
            print(order_response)
            o_id = order_response['Success']['NSE']['orderId']
            print("OrderId= ",o_id)
            netq = 99999
            status = 'OPN'
            while ((netq != 0) or (netq == 50)) and status == 'OPN':
                o_r=client.order_report(order_id = o_id)
                print(o_r)
                l1 = len(o_r['success'])
                print("Lenth = ",l1)
                netq = (o_r['success'][(l1-1)]['orderQuantity']) - (o_r['success'][(l1-1)]['filledQuantity'])
                print(netq)
                status = (o_r['success'][(l1-1)]['status'])
                time.sleep(1)
            issellniftyceotm+= 1
        print("SELL NIFTY CE Order Filled")
        if (isbuyniftyceatm == 1) & (issellniftyceotm == 1):
            print("Nifty Debit Call Spread Order Filled Successfully")
            iscespreadfilled = True
    else:
        print("There must be a open position already, Order Not placed")
    
def sell_niftyce():
    global isbuyniftyceatm
    global issellniftyceatm
    global issellniftyceotm
    global isbuyniftyceotm
    global atmceinstrumentToken
    global otmceinstrumentToken
    if iscespreadfilled == 1:
        order_response = client.place_order(order_type = "N", instrument_token = otmceinstrumentToken, transaction_type = "BUY",\
                   quantity = 50, price = 0, disclosed_quantity = 0, trigger_price = 0,\
                   tag = "python Button sellif 1", validity = "GFD", variety = "REGULAR")
        print('Buy order placed for NIFTY OTM Option CE')
        print(order_response)
        o_id = order_response['Success']['NSE']['orderId']
        print("OrderId= ",o_id)
        netq = 99999
        status = 'OPN'
        while ((netq != 0) or (netq == 50)) and status == 'OPN':
            o_r=client.order_report(order_id = o_id)
            print(o_r)
            l1 = len(o_r['success'])
            print("Lenth = ",l1)
            netq = (o_r['success'][(l1-1)]['orderQuantity']) - (o_r['success'][(l1-1)]['filledQuantity'])
            print(netq)
            status = (o_r['success'][(l1-1)]['status'])
            time.sleep(1)
        issellniftyceotm-= 1
        print("BUY NIFTY OTM CE Order Filled")
        if issellniftyceotm == 0:
            order_response = client.place_order(order_type = "N", instrument_token = atmceinstrumentToken, transaction_type = "SELL",\
                    quantity = 50, price = 0, disclosed_quantity = 0, trigger_price = 0,\
                    tag = "python Button buyif 1", validity = "GFD", variety = "REGULAR")
            print("SELL order placed for NIFTY ATM Option CE")
            print(order_response)
            o_id = order_response['Success']['NSE']['orderId']
            print("OrderId= ",o_id)
            netq = 99999
            status = 'OPN'
            while ((netq != 0) or (netq == 50)) and status == 'OPN':
                o_r=client.order_report(order_id = o_id)
                print(o_r)
                l1 = len(o_r['success'])
                print("Lenth = ",l1)
                netq = (o_r['success'][(l1-1)]['orderQuantity']) - (o_r['success'][(l1-1)]['filledQuantity'])
                print(netq)
                status = (o_r['success'][(l1-1)]['status'])
                time.sleep(1)
            isbuyniftyceatm-= 1
        print("SELL NIFTY ATM CE Order Filled")
        if (isbuyniftyceatm == 0) & (issellniftyceotm == o):
            print("Nifty Debit Call Spread EXIT Order Filled Successfully")
            iscespreadfilled = False
        else:
            print("Something went wrong while Exiting Nifty Debit Call Spread, Check Positions manually")
    else:
        print('No Nifty Debit Call Spread option to Exit')

def buy_niftype():
    global isbuyniftypeatm
    global peinstrumentToken
    if isbuyniftypeatm == 0:
        client.login(password = password)
        client.session_2fa(access_code = otp)
        quote_response = client.quote(instrument_token = underlying_token)
        ltp = quote_response['success'][0]['ltp']
        ltp = float(ltp)
        atm = round(ltp/50)*50
        print(atm)
        peinstrumentToken = df.loc[(df['instrumentName'] == 'NIFTY') & (df['expiry'] == expiry) & (df['optionType'] == 'PE') & (df['strike'] == atm), 'instrumentToken'].iloc[0]
        peinstrumentToken  = int(peinstrumentToken)
        order_response = client.place_order(order_type = "N", instrument_token = peinstrumentToken, transaction_type = "BUY",\
                   quantity = 50, price = 0, disclosed_quantity = 0, trigger_price = 0,\
                   tag = "python Button buyif 1", validity = "GFD", variety = "REGULAR")
        print("Buy order placed for NIFTY Option PE")
        print(order_response)
        o_id = order_response['Success']['NSE']['orderId']
        print("OrderId= ",o_id)
        netq = 99999
        status = 'OPN'
        while ((netq != 0) or (netq == 50)) and status == 'OPN':
            o_r=client.order_report(order_id = o_id)
            print(o_r)
            l1 = len(o_r['success'])
            print("Lenth = ",l1)
            netq = (o_r['success'][(l1-1)]['orderQuantity']) - (o_r['success'][(l1-1)]['filledQuantity'])
            print(netq)
            status = (o_r['success'][(l1-1)]['status'])
            time.sleep(1)
        isbuyniftypeatm+= 1
        print("Buy NIFTY PE Order Filled")
    
def sell_niftype():
    global isbuyniftypeatm
    global peinstrumentToken
    if isbuyniftypeatm == 1:
        order_response = client.place_order(order_type = "N", instrument_token = peinstrumentToken, transaction_type = "SELL",\
                   quantity = 50, price = 0, disclosed_quantity = 0, trigger_price = 0,\
                   tag = "python Button sellif 1", validity = "GFD", variety = "REGULAR")
        print('Sell order placed for NIFTY Option PE')
    else:
        print('No PE option to Sell')

niftyroot = Tk()
frame = Frame(niftyroot)
frame.pack()
bottomframe = Frame(niftyroot)
bottomframe.pack( side = BOTTOM )
buy_niftyce_button = Button(frame, text = 'NIFTY CE'+'\n\n'+'1', bg = 'yellow', fg ='black',height = 5, width = 15, command=buy_niftyce)
buy_niftyce_button.pack( side = LEFT)
sell_niftyce_button = Button(frame, text = 'NIFTY CE'+'\n\n'+'1', bg = 'red', fg ='black',height = 5, width = 15, command=sell_niftyce)
sell_niftyce_button.pack( side = LEFT)
buy_niftype_button = Button(bottomframe, text = 'NIFTY PE'+'\n\n'+'1', bg = 'yellow', fg ='black',height = 5, width = 15, command=buy_niftype)
buy_niftype_button.pack( side = LEFT)
sell_niftype_button = Button(bottomframe, text = 'NIFTY PE'+'\n\n'+'1', bg = 'red', fg ='black',height = 5, width = 15, command=sell_niftype)
sell_niftype_button.pack( side = LEFT)
niftyroot.attributes('-topmost',True)
niftyroot.mainloop()
from tkinter import *
from ks_api_client import ks_api
import os
from dotenv import load_dotenv
import time
# Defining the host is optional and defaults to https://tradeapi.kotaksecurities.com/apim
# See configuration.py for a list of all supported configuration parameters.
load_dotenv()
access_token = os.getenv("access_token")
userid = os.getenv("userid")
consumer_key = os.getenv("consumer_key")
password = os.getenv("password")
host = os.getenv("host")
otp = os.getenv("otp")
client = ks_api.KSTradeApi(access_token = access_token, userid = userid, \
                consumer_key = consumer_key, ip = "127.0.0.1", app_id = "", host = host)
# Get session for user
#client.login(password = password)
#otp= input("Enter OTP: ")
#Generated session token
#client.session_2fa(access_code = otp)

isbuymcx = 0
issellmcx = 0
def buy_mcx():
    global isbuymcx
    global issellmcx
    if isbuymcx == 0 and issellmcx == 0:
        client.login(password = password)
        client.session_2fa(access_code = otp)
        order_response = client.place_order(order_type = "N", instrument_token = 11163, transaction_type = "BUY",\
                   quantity = 6, price = 0, disclosed_quantity = 0, trigger_price = 0,\
                   tag = "python Button buyif 1", validity = "GFD", variety = "REGULAR")
        print("NEW Buy order placed for MCX")
        print(order_response)
        o_id = order_response['Success']['NSE']['orderId']
        print("OrderId= ",o_id)
        netq = 99999
        status = 'OPN'
        while ((netq != 0) or (netq == 6)) and status == 'OPN':
            o_r=client.order_report(order_id = o_id)
            print(o_r)
            l1 = len(o_r['success'])
            print("Lenth = ",l1)
            netq = (o_r['success'][(l1-1)]['orderQuantity']) - (o_r['success'][(l1-1)]['filledQuantity'])
            print(netq)
            status = (o_r['success'][(l1-1)]['status'])
            time.sleep(1)
        isbuymcx+= 1
        print("New Buy order Filled for MCX")
    elif issellmcx == 1 and isbuymcx ==0:
        client.login(password = password)
        client.session_2fa(access_code = otp)
        order_response = client.place_order(order_type = "N", instrument_token = 11163, transaction_type = "BUY",\
                   quantity = 6, price = 0, disclosed_quantity = 0, trigger_price = 0,\
                   tag = "python Button buyif 1", validity = "GFD", variety = "REGULAR")
        print("Exit Buy order placed for Sold MCX")
        print(order_response)
        o_id = order_response['Success']['NSE']['orderId']
        print("OrderId= ",o_id)
        netq = 99999
        status = 'OPN'
        while ((netq != 0) or (netq == 6)) and status == 'OPN':
            o_r=client.order_report(order_id = o_id)
            print(o_r)
            l1 = len(o_r['success'])
            print("Lenth = ",l1)
            netq = (o_r['success'][(l1-1)]['orderQuantity']) - (o_r['success'][(l1-1)]['filledQuantity'])
            print(netq)
            status = (o_r['success'][(l1-1)]['status'])
            time.sleep(1)
        print("Exit Buy order Filled for Sold MCX")
        isbuymcx = 0
        issellmcx = 0
    else:
        print('MCX already bought')
def sell_mcx():
    global isbuymcx
    global issellmcx
    if issellmcx == 0 and isbuymcx == 0:
        client.login(password = password)
        client.session_2fa(access_code = otp)
        order_response = client.place_order(order_type = "N", instrument_token = 11163, transaction_type = "SELL",\
                   quantity = 6, price = 0, disclosed_quantity = 0, trigger_price = 0,\
                   tag = "python Button buyif 1", validity = "GFD", variety = "REGULAR")
        print("NEW Sell order placed for MCX")
        print(order_response)
        o_id = order_response['Success']['NSE']['orderId']
        print("OrderId= ",o_id)
        netq = 99999
        status = 'OPN'
        while ((netq != 0) or (netq == 6)) and status == 'OPN':
            o_r=client.order_report(order_id = o_id)
            print(o_r)
            l1 = len(o_r['success'])
            print("Lenth = ",l1)
            netq = (o_r['success'][(l1-1)]['orderQuantity']) - (o_r['success'][(l1-1)]['filledQuantity'])
            print(netq)
            status = (o_r['success'][(l1-1)]['status'])
            time.sleep(1)
        print('New Sell order placed for mcx')
        issellmcx+= 1
    elif isbuymcx == 1 and issellmcx ==0:
        client.login(password = password)
        client.session_2fa(access_code = otp)
        order_response = client.place_order(order_type = "N", instrument_token = 11163, transaction_type = "SELL",\
                   quantity = 6, price = 0, disclosed_quantity = 0, trigger_price = 0,\
                   tag = "python Button buyif 1", validity = "GFD", variety = "REGULAR")
        print("Exit Sell order placed for Bought MCX")
        print(order_response)
        o_id = order_response['Success']['NSE']['orderId']
        print("OrderId= ",o_id)
        netq = 99999
        status = 'OPN'
        while ((netq != 0) or (netq == 6)) and status == 'OPN':
            o_r=client.order_report(order_id = o_id)
            print(o_r)
            l1 = len(o_r['success'])
            print("Lenth = ",l1)
            netq = (o_r['success'][(l1-1)]['orderQuantity']) - (o_r['success'][(l1-1)]['filledQuantity'])
            print(netq)
            status = (o_r['success'][(l1-1)]['status'])
            time.sleep(1)
        print('Exit Buy order filled for MCX')
        isbuysilvermic = 0
        issellsilvermic = 0
    else:
        print('MCX already sold')

root = Tk()
frame = Frame(root)
frame.pack()
bottomframe = Frame(root)
bottomframe.pack( side = BOTTOM )
buy_mcx_button = Button(frame, text = 'MCX'+'\n\n'+'6', bg = 'green', fg ='black',height = 5, width = 15, command=buy_mcx)
buy_mcx_button.pack( side = LEFT)
sell_mcx_button = Button(frame, text = 'MCX'+'\n\n'+'6', bg = 'red', fg ='black',height = 5, width = 15, command=sell_mcx)
sell_mcx_button.pack( side = LEFT)
root.attributes('-topmost',True)
root.mainloop()
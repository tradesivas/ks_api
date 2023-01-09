from tkinter import *
from asyncio.windows_events import NULL
import ks_api_client
from ks_api_client import ks_api
import os
from dotenv import load_dotenv
# Defining the host is optional and defaults to https://tradeapi.kotaksecurities.com/apim
# See configuration.py for a list of all supported configuration parameters.
load_dotenv()
access_token = os.getenv("access_token")
userid = os.getenv("userid")
consumer_key = os.getenv("consumer_key")
password = os.getenv("password")
host = os.getenv("host")
#client = ks_api.KSTradeApi(access_token = access_token, userid = userid, \
#                consumer_key = consumer_key, ip = "127.0.0.1", app_id = "", host = host)
# Get session for user
#client.login(password = password)
#otp= input("Enter OTP: ")
#Generated session token
#client.session_2fa(access_code = otp)

isbuysilvermic = 0
issellsilvermic = 0
def buy_silvermic():
    global isbuysilvermic
    global issellsilvermic
    if isbuysilvermic == 0 and issellsilvermic == 0:
        client.place_order(order_type = "N", instrument_token = 4059, transaction_type = "BUY",\
                   quantity = 1, price = 0, disclosed_quantity = 0, trigger_price = 0,\
                   tag = "python Button buyif 1", validity = "GFD", variety = "REGULAR")
        print('Buy order placed for silvermic')
        isbuysilvermic+= 1
    elif issellsilvermic == 1 and isbuysilvermic ==0:
        client.place_order(order_type = "N", instrument_token = 4059, transaction_type = "BUY",\
                   quantity = 1, price = 0, disclosed_quantity = 0, trigger_price = 0,\
                   tag = "python Button buyif 2", validity = "GFD", variety = "REGULAR")
        print('sell order closed for Silvermic')
        isbuysilvermic = 0
        issellsilvermic = 0
    else:
        print('Silvermic already bought')
def sell_silvermic():
    global isbuysilvermic
    global issellsilvermic
    if issellsilvermic == 0 and isbuysilvermic == 0:
        client.place_order(order_type = "N", instrument_token = 4059, transaction_type = "SELL",\
                   quantity = 1, price = 0, disclosed_quantity = 0, trigger_price = 0,\
                   tag = "python Button sellif 1", validity = "GFD", variety = "REGULAR")
        print('Sell order placed for silvermic')
        issellsilvermic+= 1
    elif isbuysilvermic == 1 and issellsilvermic ==0:
        client.place_order(order_type = "N", instrument_token = 4059, transaction_type = "SELL",\
                   quantity = 1, price = 0, disclosed_quantity = 0, trigger_price = 0,\
                   tag = "python Button sellif 2", validity = "GFD", variety = "REGULAR")
        print('Buy order closed for Silvermic')
        isbuysilvermic = 0
        issellsilvermic = 0
    else:
        print('Silvermic already sold')

root = Tk()
frame = Frame(root)
frame.pack()
bottomframe = Frame(root)
bottomframe.pack( side = BOTTOM )
buy_silvermic_button = Button(frame, text = 'silvermic'+'\n\n'+'1', bg = 'green', fg ='black',height = 5, width = 15, command=buy_silvermic)
buy_silvermic_button.pack( side = LEFT)
sell_silvermic_button = Button(frame, text = 'silvermic'+'\n\n'+'1', bg = 'red', fg ='black',height = 5, width = 15, command=sell_silvermic)
sell_silvermic_button.pack( side = LEFT)
buy_bankbees_button = Button(bottomframe, text = 'Bankbees'+'\n\n'+'1', bg = 'green', fg ='black',height = 5, width = 15)
buy_bankbees_button.pack( side = LEFT)
sell_bankbees_button = Button(bottomframe, text = 'Bankbees'+'\n\n'+'1', bg = 'red', fg ='black',height = 5, width = 15)
sell_bankbees_button.pack( side = LEFT)
buy_tatapower_button = Button(bottomframe, text = 'Tatapower'+'\n\n'+'1', bg = 'green', fg ='black',height = 5, width = 15)
buy_tatapower_button.pack( side = LEFT)
root.attributes('-topmost',True)
root.mainloop()
#Run This Code at 9:20:01 AM on Market Open Days
#Floating Band Strategy in 5 min candle sticks

from operator import truediv
import tvDatafeed
import pandas as pd
import os
import datetime
import pause
import time
import mplfinance as mpf
from tvDatafeed import TvDatafeed,Interval
from datetime import datetime, date

import ks_api_client
from ks_api_client import ks_api
from dotenv import load_dotenv

load_dotenv()
access_token = os.getenv("access_token")
userid = os.getenv("userid")
consumer_key = os.getenv("consumer_key")
password = os.getenv("password")
host = os.getenv("host")
client = ks_api.KSTradeApi(access_token = access_token, userid = userid, \
                consumer_key = consumer_key, ip = "127.0.0.1", app_id = "", host = host)
# Get session for user
client.login(password = password)
otp= input("Enter OTP: ")
#Generated session token
client.session_2fa(access_code = otp)

class ANSI():
    def background(code):
        return "\33[{code}m".format(code=code)
  
    def style_text(code):
        return "\33[{code}m".format(code=code)
  
    def color_text(code):
        return "\33[{code}m".format(code=code)
buy_ansi = ANSI.color_text(42)+ "BUY qty = "
sell_ansi = ANSI.color_text(41)+ "SELL qty = "


tv=TvDatafeed()
now = datetime.now()
print_time = now.strftime("%H:%M:%S")
print("Program Started at ", print_time)
buyopen  = False
sellopen = False
buyqty = 1
sellqty = 1
i = 1
while i < 74:
    #time.sleep(300) # waiting for 5 min to current candle complete
    for j in range(299,-1,-1):
        print("waiting for candle to complete ", f"{j}  ", end="\r", flush=True)
        time.sleep(1)
    data = tv.get_hist(symbol='bankbees',exchange='nse',interval=Interval.in_5_minute,n_bars=3)
    print(data)
    now = datetime.now()
    print_time = now.strftime("%H:%M:%S")
    prehi = data.iloc[-3,2]
    prelo = data.iloc[-3,3]
    predif = round(abs(prehi-prelo),2)
    preub = round(prehi+predif, 2)
    prelb = round(prelo-predif, 2)
    close = data.iloc[-2,4]
    print("Prehi= ",prehi, "   prelo= ", prelo, "   predif= ", predif, "preub= ", preub, "prelb= ", prelb, "close= ", close)
    if close > preub and buyopen == False:
        if sellopen == False:
            buyqty = 1
        elif sellopen == True:
            buyqty = 2
        print(i, buy_ansi, buyqty)
        #Placing order with Kotak Securities Ltd.
        client.place_order(order_type = "N", instrument_token = 4059, transaction_type = "BUY",\
                   quantity = buyqty, price = 0, disclosed_quantity = 0, trigger_price = 0,\
                   tag = "Order_By_Python_2_py", validity = "GFD", variety = "REGULAR")
        buyopen = True
        sellopen = False
    elif close < prelb and sellopen == False:
        if buyopen == False:
            sellqty = 1
        elif buyopen == True:
            sellqty = 2
        print(i, sell_ansi, sellqty)
        client.place_order(order_type = "N", instrument_token = 4059, transaction_type = "SELL",\
                   quantity = sellqty, price = 0, disclosed_quantity = 0, trigger_price = 0,\
                   tag = "Order_By_Python_2_py", validity = "GFD", variety = "REGULAR")
        sellopen = True
        buyopen = False
    else:
        print(i, "waiting for signal")
    print("Print Time =", print_time)
    i += 1
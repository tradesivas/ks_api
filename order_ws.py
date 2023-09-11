import os
from dotenv import load_dotenv
import pandas as pd
import time
import logging
from ks_api_client import ks_api

logging.basicConfig(level=logging.INFO)
load_dotenv()
access_token = os.getenv("access_token")
userid = os.getenv("userid")
consumer_key = os.getenv("consumer_key")
consumer_secret = os.getenv("consumer_secret")
password = os.getenv("password")
host = os.getenv("host")
otp = os.getenv("otp")

client = ks_api.KSTradeApi(access_token = access_token, userid = userid,
                            consumer_key = consumer_key, consumer_secret = consumer_secret, ip = "127.0.0.1", app_id = "", host = host)

def login(client, password, otp):
    try:
        client.login(password = password)
        client.session_2fa(access_code = otp)
    except Exception as e:
        print("Exception when Login: %s\n" % e)

def callback_method(message):
        # ltp = float(message[6])
        # time = message[19]
        # print("LTP is: ",ltp)
        # print("Time is ", time)
        print(message)
        

login(client, password, otp)
client.subscribe(input_tokens="11691", callback=callback_method, broadcast_host="https://wstreamer.kotaksecurities.com/feed/orders")
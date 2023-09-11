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

def get_position_data(client):
    try:
        # Get's position by position_type.
        o_position = client.positions(position_type = "OPEN")
        return o_position
    except Exception as e:
        print("Exception when calling PositionsApi->positions: %s\n" % e)

def place_stop_loss_order(client, order_type, instrument_token, transaction_type, quantity, trigger_price, instrumentName):
    try:
        order_response = client.place_order(order_type = order_type, instrument_token = instrument_token, transaction_type = transaction_type,
                                       quantity = quantity, price = 0, disclosed_quantity = 0, trigger_price = trigger_price,
                                       tag = "python sl order", validity = "GFD", variety = "REGULAR")
        return order_response
    except Exception as e:
        print("Exception when Placing Order for " + instrumentName + " of " + quantity + " qyt at " + trigger_price + " OrderApi->Order: %s\n" % e)

if __name__ == "__main__":
    login(client, password, otp)
    o_position = get_position_data(client)
    isslplaced = False
    for position in o_position['Success']:
        instrumentName = position['instrumentName']
        netTrdQty = position['netTrdQtyLot']
        if netTrdQty != 0:
            instrument_token = position['instrumentToken']
            sellOpenQtyLot = position['sellOpenQtyLot']
            buyOpenQtyLot = position['buyOpenQtyLot']
            if netTrdQty > 0:
                transaction_type = "SELL"
                order_type = "N"
                quantity = netTrdQty - sellOpenQtyLot
            elif netTrdQty < 0:
                transaction_type = "BUY"
                order_type = "MIS"
                quantity = abs(netTrdQty) - buyOpenQtyLot
            else:
                quantity = 0
            if quantity > 0:
                trigger_price = float(input("SL Trigger Price for " + instrumentName + " :"))
                order_response = place_stop_loss_order(client, order_type, instrument_token, transaction_type, quantity, trigger_price, instrumentName)
                order_id = order_response['Success']['NSE']['orderId']
                isslplaced = True
            else:
                print(instrumentName + "          SL order already Placed")
        else:
            print(instrumentName + "          No Open Position")

if isslplaced == True:
    tgp = float(input("Target Price for " + instrumentName + " :"))

    def callback_method(message):
        ltp = float(message[6])
        print(instrumentName + " TGP is: ",tgp)
        print(instrumentName + " LTP is: ",ltp)
        if transaction_type == "SELL":
            if ltp >= tgp:
                trigger_price = 0
                order_response = place_stop_loss_order(client, order_type, instrument_token, transaction_type, quantity, trigger_price, instrumentName)
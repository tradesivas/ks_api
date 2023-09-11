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

client.login(password = password)
client.session_2fa(access_code = otp)

def get_position_data(client):
    try:
        # Get's position by position_type.
        o_position = client.positions(position_type = "OPEN")
        return o_position
    except Exception as e:
        print("Exception when calling PositionsApi->positions: %s\n" % e)

def place_stop_loss_order(client, position, trigger_price):
    transaction_type = "SELL" if position['netTrdQtyLot'] > 0 else "BUY"
    order_type = "N" if position['netTrdQtyLot'] > 0 else "MIS"
    quantity = abs(position['netTrdQtyLot'])
    order_response = client.place_order(order_type = order_type, instrument_token = position['instrumentToken'], transaction_type = transaction_type,
                                       quantity = quantity, price = 0, disclosed_quantity = 0, trigger_price = trigger_price,
                                       tag = "python sl order", validity = "GFD", variety = "REGULAR")
    return order_response

if __name__ == "__main__":
    o_position = get_position_data(client)
    for position in o_position['Success']:
        instrumentName = position['instrumentName']
        trigger_price = float(input("SL Trigger Price for " + instrumentName + " :"))
        order_response = place_stop_loss_order(client, position, trigger_price)
        print(order_response)
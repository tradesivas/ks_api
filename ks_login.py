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
client = ks_api.KSTradeApi(access_token = access_token, userid = userid, \
                consumer_key = consumer_key, ip = "127.0.0.1", app_id = "", host = host)
# Get session for user
login_response = client.login(password = password)
print("---------------login response---------------")
print(login_response)
newotp= input("Enter NEW OTP: ")

#Generated session token
session_response = client.session_2fa(access_code = newotp)
print("---------------session response---------------")
print(session_response)
#quote = client.quote(instrument_token = 110)
#print(quote)
#client.place_order(order_type = "N", instrument_token = 3867, transaction_type = "BUY", quantity = 1, price = 180, \
                   #disclosed_quantity = 0, trigger_price = 0, tag = "ks_login_py", validity = "GFD", variety = "REGULAR", \
                   #product = "NORMAL" ,smart_order_routing="string")
#order_report = client.order_report()
#print(order_report)
logout_response = client.logout()
print("---------------logout response---------------")
print(logout_response)
from ks_api_client import ks_api
import os
from dotenv import load_dotenv
load_dotenv()
################################################
access_token = os.getenv("access_token")
userid = os.getenv("userid")
consumer_key = os.getenv("consumer_key")
password = os.getenv("password")
otp = os.getenv("otp")
host = os.getenv("host")
##############################################
client = ks_api.KSTradeApi(access_token = access_token, userid = userid, \
                consumer_key = consumer_key, ip = "127.0.0.1", app_id = "", host = host)
login_response = client.login(password = password)
################################################
tg_or_id = input("Enter Target order id: ")
high = input("Enter Swing High Price: ")
####################################################

session_response = client.session_2fa(access_code = otp)
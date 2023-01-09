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
otp = os.getenv("otp")
client = ks_api.KSTradeApi(access_token = access_token, userid = userid, \
                consumer_key = consumer_key, ip = "127.0.0.1", app_id = "", host = host)
# Get session for user
client.login(password = password)

#Generated session token
client.session_2fa(access_code = otp)
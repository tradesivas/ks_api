from ks_api_client import ks_api
import os
from dotenv import load_dotenv
# Defining the host is optional and defaults to https://tradeapi.kotaksecurities.com/apim
# See configuration.py for a list of all supported configuration parameters.
load_dotenv()
access_token = os.getenv("access_token")
userid = os.getenv("userid")
consumer_key = os.getenv("consumer_key")
consumer_secret = os.getenv("consumer_secret")
password = os.getenv("password")
host = os.getenv("host")
otp = os.getenv("otp")
client = ks_api.KSTradeApi(access_token = access_token, userid = userid, \
                consumer_key = consumer_key,consumer_secret = consumer_secret, ip = "127.0.0.1", app_id = "", host = host)
# Get session for user
login_response = client.login(password = password)
print("---------------login response---------------")
print(login_response)
#Generated session token
print("OTp is: ",otp)
session_response = client.session_2fa(access_code = otp)
print("---------------session response---------------")
print(session_response)

#Subscribing to Streaming Websocket
try:
    def callback_method(message):
        print(message)
        print("Your logic/computation will come here.")
    # subscribe to the streamingAPI
    client.subscribe(input_tokens="11721", callback=callback_method, broadcast_host="https://wstreamer.kotaksecurities.com/feed")
except Exception as e:
    print("Exception when calling StreamingApi->subscribe: %s\n" % e)


#Unsubscribing to Streaming Websocket
try:
    # unsubscribe to the streamingAPI
    client.unsubscribe()
except Exception as e: 
    print("Exception when calling StreamingApi->unsubscribe: %s\n" % e)
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
logout_response = client.logout()
print("---------------logout response---------------")
print(logout_response)
#Storing New OPT to .env file
oldotp = os.getenv("otp")
with open(".env",'r') as file :
        filedata = file.read()
filedata = filedata.replace(oldotp,newotp)
with open(".env",'w') as file :
        file.write(filedata)
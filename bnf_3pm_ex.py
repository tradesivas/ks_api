from ks_api_client import ks_api
import os
from dotenv import load_dotenv
import pandas as pd
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
print("OTP is: ",otp)
session_response = client.session_2fa(access_code = otp)
print("---------------session response---------------")
print(session_response)

#Subscribing to Streaming Websocket
#df = pd.DataFrame(columns=['null_0', 'null_1', 'null_2', 'null_3', 'null_4', 'null_5', 'ltp', 'null_7',
                            #  'null_8', 'null_9', 'null_10', 'null_11', 'null_12', 'null_13', 'null_14', 'null_15',
                            #   'null_16', 'null_17', 'null_18', 'null_19', 'null_20', 'null_21', 'null_22', 'null_23', 'null_24'])
message1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]#,0,0]
df1 = pd.DataFrame([message1])
df1.columns = ['null_0', 'null_1', 'null_2', 'null_3', 'null_4', 'null_5', 'ltp', 'null_7', \
                'null_8', 'null_9', 'null_10', 'null_11', 'null_12', 'null_13', 'null_14', 'null_15', \
                'null_16', 'null_17', 'null_18', 'null_19', 'null_20', 'null_21', 'null_22']#, 'null_23', 'null_24']
issell = 0

try:
    def callback_method(message):
        #print(message)
        global df, df1, ltp, celtp, peltp, issell, cesold, pesold
        #print("Your logic/computation will come here.")
        #print(type(message))
        df = pd.DataFrame([message])
        df.columns = ['null_0', 'null_1', 'null_2', 'null_3', 'null_4', 'null_5', 'ltp', 'null_7', \
                'null_8', 'null_9', 'null_10', 'null_11', 'null_12', 'null_13', 'null_14', 'null_15', \
                'null_16', 'null_17', 'null_18', 'null_19', 'null_20', 'null_21', 'null_22']#, 'null_23', 'null_24']
        #ltp = float(message[6])
        # if ltp > 17712:
        #     print("Nifty Greater than 17712")
        #print("LTP is: ",ltp)
        df1 = pd.concat([df,df1])
        print(df1)
        peltp = float(df1.loc[(df1['null_1'] == '24391'), 'null_2'].iloc[0])
        celtp = float(df1.loc[(df1['null_1'] == '23493'), 'null_2'].iloc[0])
        print(peltp)
        print(celtp)
        if (celtp < (peltp/4)) and (celtp < 7) and issell == 0:
            print("Sell CE")
            issell = 1
            cesold = celtp
        elif (peltp < (celtp/4)) and (peltp < 7) and issell == 0:
            print("Sell PE")
            issell = 2
            pesold = peltp
        elif issell == 1:
            print("Sold CE")
            print("P&L= ",((cesold - celtp)*40) )
        elif issell == 2:
            print("Sold PE")
            print("P&L= ",((pesold - peltp)*40) )
        else:
            print("No TRADE")
        #df.to_csv(r"data\data.txt", sep=',', mode='a', header = False)
    # subscribe to the streamingAPI
    client.subscribe(input_tokens="24391,23493", callback=callback_method, broadcast_host="https://wstreamer.kotaksecurities.com/feed")

except Exception as e:
    print("Exception when calling StreamingApi->subscribe: %s\n" % e)


#Unsubscribing to Streaming Websocket
try:
    # unsubscribe to the streamingAPI
    client.unsubscribe()
except Exception as e: 
    print("Exception when calling StreamingApi->unsubscribe: %s\n" % e)
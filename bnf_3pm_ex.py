from ks_api_client import ks_api
import os
from dotenv import load_dotenv
import pandas as pd

#####################################################################

load_dotenv()
access_token = os.getenv("access_token")
userid = os.getenv("userid")
consumer_key = os.getenv("consumer_key")
consumer_secret = os.getenv("consumer_secret")
password = os.getenv("password")
host = os.getenv("host")
otp = os.getenv("otp")

#####################################################################
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

############################################################################

cash = pd.read_csv ("ks_cash_scripmaster.txt",sep="|")
fno = pd.read_csv ("ks_fno_scripmaster.txt",sep="|")
expiry = os.getenv("banknifty_expiry")
instrumentName = 'BANKNIFTY'
underlying_name = 'NIFTY BANK'
max_opt_price = 10
lot = 25
underlying_token  = cash.loc[(cash['instrumentName'] == underlying_name) & (cash['instrumentType'] == 'IN') & (cash['segment'] == '-') & (cash['exchange'] == 'NSE'), 'instrumentToken'].iloc[0]
underlying_token  = int(underlying_token)
client.login(password = password)
client.session_2fa(access_code = otp)
quote_response = client.quote(instrument_token = underlying_token)
ltp = quote_response['success'][0]['ltp']
ltp = float(ltp)
atm = round(ltp/100)*100
print(atm)
ceinstrumentToken = fno.loc[(fno['instrumentName'] == 'BANKNIFTY') & (fno['expiry'] == expiry) & (fno['optionType'] == 'CE') & (fno['strike'] == atm), 'instrumentToken'].iloc[0]
ceinstrumentToken  = int(ceinstrumentToken)
peinstrumentToken = fno.loc[(fno['instrumentName'] == 'BANKNIFTY') & (fno['expiry'] == expiry) & (fno['optionType'] == 'PE') & (fno['strike'] == atm), 'instrumentToken'].iloc[0]
peinstrumentToken  = int(peinstrumentToken)

##############################################################################

message1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
df1 = pd.DataFrame([message1])
df1.columns = ['null_0', 'opt_token', 'null_2', 'null_3', 'null_4', 'null_5', 'ltp', 'null_7', \
                'null_8', 'null_9', 'null_10', 'null_11', 'null_12', 'null_13', 'null_14', 'null_15', \
                'null_16', 'null_17', 'null_18', 'null_19', 'null_20', 'null_21', 'null_22']

##############################################################################
issell = 0
try:
    def callback_method(message):
        #print(message)
        global df, df1, ltp, celtp, peltp, issell, cesold, pesold
        #print("Your logic/computation will come here.")
        #print(type(message))
        df = pd.DataFrame([message])
        df.columns = ['null_0', 'opt_token', 'null_2', 'null_3', 'null_4', 'null_5', 'ltp', 'null_7', \
                'null_8', 'null_9', 'null_10', 'null_11', 'null_12', 'null_13', 'null_14', 'null_15', \
                'null_16', 'null_17', 'null_18', 'null_19', 'null_20', 'null_21', 'null_22']
        #ltp = float(message[6])
        # if ltp > 17712:
        #     print("Nifty Greater than 17712")
        #print("LTP is: ",ltp)
        df1 = pd.concat([df,df1])
        print(df1)
        celtp = float(df1.loc[(df1['opt_token'] == ceinstrumentToken), 'null_2'].iloc[0])
        peltp = float(df1.loc[(df1['opt_token'] == peinstrumentToken), 'null_2'].iloc[0])
        print("CE LTP = ", celtp)
        print("PE LTP = ", peltp)
        if (celtp < (peltp/4)) and (celtp < max_opt_price) and issell == 0:
            ###################################################
            order_response = client.place_order(order_type = "N", instrument_token = ceinstrumentToken, transaction_type = "SELL",\
                   quantity = lot, price = 0, disclosed_quantity = 0, trigger_price = 0,\
                   tag = "bnf_3pm_ex.py | Entry for Sell CE", validity = "GFD", variety = "REGULAR")
            print("Sell order placed for BANKNIFTY Option CE")
            print(order_response)
            o_id = order_response['Success']['NSE']['orderId']
            print("OrderId= ",o_id)
            netq = 99999
            status = 'OPN'
            while ((netq != 0) or (netq == lot)) and status == 'OPN':
                o_r=client.order_report(order_id = o_id)
                print(o_r)
                l1 = len(o_r['success'])
                print("Lenth = ",l1)
                netq = (o_r['success'][(l1-1)]['orderQuantity']) - (o_r['success'][(l1-1)]['filledQuantity'])
                print(netq)
                status = (o_r['success'][(l1-1)]['status'])
                time.sleep(1)
            print("Sell BANKNIFTY CE Order Filled")
                            ###########
            order_response = client.place_order(order_type = "N", instrument_token = ceinstrumentToken, transaction_type = "Buy",\
                   quantity = lot, price = 0, disclosed_quantity = 0, trigger_price = (2.5*cesold),\
                   tag = "bnf_3pm_ex.py | SL for CE sold", validity = "GFD", variety = "REGULAR")

            ###################################################
            print("Sell order placed for CE at Rs.", celtp, " * ", lot, " = Rs.", (celtp*lot))
            issell = 1
            cesold = celtp
        elif (peltp < (celtp/4)) and (peltp < max_opt_price) and issell == 0:
            print("Sell order placed for PE at Rs.", peltp, " * ", lot, " = Rs.", (peltp*lot))
            issell = 2
            pesold = peltp
        elif issell == 1:
            print("Already Sold CE at Rs.", cesold, " * ", lot, " = Rs.", (cesold*lot)")
            print("P&L= Rs.",((cesold - celtp)*lot) )
        elif issell == 2:
            print("Already Sold PE")
            print("P&L= Rs.",((pesold - peltp)*lot) )
        else:
            print("No TRADE")

    client.subscribe(input_tokens=ceinstrumentToken,peinstrumentToken, callback=callback_method, broadcast_host="https://wstreamer.kotaksecurities.com/feed")

except Exception as e:
    print("Exception when calling StreamingApi->subscribe: %s\n" % e)


#Unsubscribing to Streaming Websocket
try:
    # unsubscribe to the streamingAPI
    client.unsubscribe()
except Exception as e: 
    print("Exception when calling StreamingApi->unsubscribe: %s\n" % e)
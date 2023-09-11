from ks_api_client import ks_api
import os
from dotenv import load_dotenv
import pandas as pd
import time

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
#print("---------------login response---------------")
#print(login_response)
#Generated session token
session_response = client.session_2fa(access_code = otp)
#print("---------------session response---------------")
#print(session_response)

############################################################################
try:
    # Get's position by position_type.
    o_position = client.positions(position_type = "OPEN")
    print(o_position)
except Exception as e:
    print("Exception when calling PositionsApi->positions: %s\n" % e)

############################################################################

l1 = len(o_position['Success'])
print("Lenth = ",l1)
print("---------------------------------------------")
p = 0
while p <= (l1-1):
    positions = [(o_position['Success'][(p)]['instrumentToken']), (o_position['Success'][(p)]['instrumentName']), (o_position['Success'][(p)]['netTrdQtyLot'])]
    print(positions)
    yn = input("sltg order for "+ (o_position['Success'][(p)]['instrumentName']) + " ? (y or n): ")
    if yn == 'y' and (o_position['Success'][(p)]['netTrdQtyLot']) != 0:
        trigger_price = float(input("SL Trigger Price: "))
        if (o_position['Success'][(p)]['netTrdQtyLot']) > 0:
            transaction_type = "SELL"
        elif (o_position['Success'][(p)]['netTrdQtyLot']) < 0:
            transaction_type = "BUY"
        print("sl order placed for | " + (o_position['Success'][(p)]['instrumentName']) + " | qty of " + str((o_position['Success'][(p)]['netTrdQtyLot'])) + " | at " + str(trigger_price))
        order_response = client.place_order(order_type = "N", instrument_token = (o_position['Success'][(p)]['instrumentToken']) , transaction_type = transaction_type,\
                   quantity = (o_position['Success'][(p)]['netTrdQtyLot']), price = 0, disclosed_quantity = 0, trigger_price = trigger_price,\
                   tag = "python sltg order", validity = "GFD", variety = "REGULAR")
        p = l1
    print("---------------------------------------------")
    p+= 1

############################################################################

print(order_response)























cash = pd.read_csv ("ks_cash_scripmaster.txt",sep="|")
#fno = pd.read_csv ("ks_fno_scripmaster.txt",sep="|")
#expiry = os.getenv("banknifty_expiry")
instrumentName = input("Enter Symbol: ").upper()
exchange = 'NSE'
#underlying_name = 'NIFTY BANK'
#max_opt_price = 9.5
#lot = 25
qty = input("Enter Qty: ")
open_position = input("1 for long, 2 for short: ")

############################################################################

# underlying_token  = cash.loc[(cash['instrumentName'] == underlying_name) & (cash['instrumentType'] == 'IN') & (cash['segment'] == '-') & (cash['exchange'] == 'NSE'), 'instrumentToken'].iloc[0]
# underlying_token  = int(underlying_token)
# client.login(password = password)
# client.session_2fa(access_code = otp)
# quote_response = client.quote(instrument_token = underlying_token)
# ltp = quote_response['success'][0]['ltp']
# ltp = float(ltp)
# atm = round(ltp/100)*100
# strike = str(atm)
#print(atm)
instrumentToken = str(cash.loc[(cash['instrumentName'] == instrumentName) & (cash['exchange'] == exchange), 'instrumentToken'].iloc[0])
#print("type = ", type(ceinstrumentToken))
instrumentToken_int  = int(instrumentToken)
#print("type ", type(ceinstrumentToken_int))
# peinstrumentToken = str(fno.loc[(fno['instrumentName'] == 'BANKNIFTY') & (fno['expiry'] == expiry) & (fno['optionType'] == 'PE') & (fno['strike'] == atm), 'instrumentToken'].iloc[0])
# peinstrumentToken_int  = int(peinstrumentToken)
# ws_token = ceinstrumentToken + ',' + peinstrumentToken

##############################################################################

# message1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
# df1 = pd.DataFrame([message1])
# df1.columns = ['null_0', 'opt_token', 'null_2', 'null_3', 'null_4', 'null_5', 'ltp', 'null_7', \
#                 'null_8', 'null_9', 'null_10', 'null_11', 'null_12', 'null_13', 'null_14', 'null_15', \
#                 'null_16', 'null_17', 'null_18', 'null_19', 'null_20', 'null_21', 'null_22']

##############################################################################
issell = 0
try:
    def callback_method(message):
        #print(message)
        global df, df1, ltp, celtp, peltp, issell, cesold, pesold, stradle_premium, sold_stradle_premium
        #print("Your logic/computation will come here.")
        print(type(message))
        # df = pd.DataFrame([message])
        # df.columns = ['null_0', 'opt_token', 'null_2', 'null_3', 'null_4', 'null_5', 'ltp', 'null_7', \
        #         'null_8', 'null_9', 'null_10', 'null_11', 'null_12', 'null_13', 'null_14', 'null_15', \
        #         'null_16', 'null_17', 'null_18', 'null_19', 'null_20', 'null_21', 'null_22']
        ltp = float(message[6])
        # if ltp > 17712:
        #     print("Nifty Greater than 17712")
        #print("LTP is: ",ltp)
        df1 = pd.concat([df,df1])
        #print(df1)
        celtp = float(df1.loc[(df1['opt_token'] == ceinstrumentToken), 'null_2'].iloc[0])
        peltp = float(df1.loc[(df1['opt_token'] == peinstrumentToken), 'null_2'].iloc[0])
        stradle_premium = celtp + peltp
        print(strike,"CE LTP = ", celtp)
        print(strike,"PE LTP = ", peltp)
        print("Stradle Premium = ", stradle_premium)
        ###################################################################################
        if issell == 0:
            ###################################################
            # order_response = client.place_order(order_type = "N", instrument_token = ceinstrumentToken_int, transaction_type = "SELL",\
            #        quantity = lot, price = 0, disclosed_quantity = 0, trigger_price = 0,\
            #        tag = "bnf_3pm_ex.py", validity = "GFD", variety = "REGULAR")
            # print("Sell order placed for BANKNIFTY Option CE")
            # print(order_response)
            # o_id = order_response['Success']['NSE']['orderId']
            # print("OrderId= ",o_id)
            # netq = 99999
            # while netq != 0:
            #     o_r=client.order_report(order_id = o_id)
            #     print(o_r)
            #     l1 = len(o_r['success'])
            #     print("Lenth = ",l1)
            #     netq = (o_r['success'][(l1-1)]['orderQuantity']) - (o_r['success'][(l1-1)]['filledQuantity'])
            #     print(netq)
            #     time.sleep(1)
            print("Sell order Filled for CE at Rs.", celtp, " * ", lot, " = Rs.", (celtp*lot))
            print("Sell order filled for PE at Rs.", peltp, " * ", lot, " = Rs.", (peltp*lot))
            issell = 1
            cesold = celtp
            pesold = peltp
            sold_stradle_premium = cesold + pesold
            print("Premium Collected = ", "%.2f" % (sold_stradle_premium * lot))     
                            ###########
            # sl_order_response = client.place_order(order_type = "N", instrument_token = ceinstrumentToken_int, transaction_type = "Buy",\
            #        quantity = lot, price = 0, disclosed_quantity = 0, trigger_price = (2.5*cesold),\
            #        tag = "bnf_3pm_ex.py", validity = "GFD", variety = "REGULAR")

            ###################################################

        elif issell == 1:
            print("Already Sold stradle at Rs.", sold_stradle_premium, " * ", lot, " = Rs.", "%.2f" % (sold_stradle_premium*lot))
            print("P&L= Rs.", "%.2f" % ((sold_stradle_premium - stradle_premium)*lot) )
        else:
            print("No TRADE")
        ########################################################
    client.subscribe(input_tokens=instrumentToken, callback=callback_method, broadcast_host="https://wstreamer.kotaksecurities.com/feed")

except Exception as e:
    print("Exception when calling StreamingApi->subscribe: %s\n" % e)


#Unsubscribing to Streaming Websocket
# try:
#     # unsubscribe to the streamingAPI
#     client.unsubscribe()
# except Exception as e: 
#     print("Exception when calling StreamingApi->unsubscribe: %s\n" % e)
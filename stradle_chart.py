from ks_api_client import ks_api
import os
from dotenv import load_dotenv
import pandas as pd
import time
from datetime import datetime
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# from matplotlib import style

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
login_response = client.login(password = password)
session_response = client.session_2fa(access_code = otp)

############################################################################

cash = pd.read_csv ("ks_cash_scripmaster.txt",sep="|")
fno = pd.read_csv ("ks_fno_scripmaster.txt",sep="|")
expiry = os.getenv("banknifty_expiry")
instrumentName = 'BANKNIFTY'
underlying_name = 'NIFTY BANK'
max_opt_price = 9.5
lot = 25

############################################################################

underlying_token  = cash.loc[(cash['instrumentName'] == underlying_name) & (cash['instrumentType'] == 'IN') & (cash['segment'] == '-') & (cash['exchange'] == 'NSE'), 'instrumentToken'].iloc[0]
underlying_token  = int(underlying_token)
client.login(password = password)
client.session_2fa(access_code = otp)
quote_response = client.quote(instrument_token = underlying_token)
ltp = quote_response['success'][0]['ltp']
ltp = float(ltp)
atm = round(ltp/100)*100
strike = str(atm)
#print(atm)
ceinstrumentToken = str(fno.loc[(fno['instrumentName'] == 'BANKNIFTY') & (fno['expiry'] == expiry) & (fno['optionType'] == 'CE') & (fno['strike'] == atm), 'instrumentToken'].iloc[0])
#print("type = ", type(ceinstrumentToken))
ceinstrumentToken_int  = int(ceinstrumentToken)
#print("type ", type(ceinstrumentToken_int))
peinstrumentToken = str(fno.loc[(fno['instrumentName'] == 'BANKNIFTY') & (fno['expiry'] == expiry) & (fno['optionType'] == 'PE') & (fno['strike'] == atm), 'instrumentToken'].iloc[0])
peinstrumentToken_int  = int(peinstrumentToken)
ws_token = ceinstrumentToken + ',' + peinstrumentToken

##############################################################################

message1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
df1 = pd.DataFrame([message1])
df1.columns = ['null_0', 'opt_token', 'null_2', 'null_3', 'null_4', 'null_5', 'ltp', 'null_7', \
                'null_8', 'null_9', 'null_10', 'null_11', 'null_12', 'null_13', 'null_14', 'null_15', \
                'null_16', 'null_17', 'null_18', 'null_19', 'null_20', 'null_21', 'null_22']
pldf1 = pd.DataFrame(data={'time':[''],'pnl':['']})

##############################################################################
t = 0

###############################################################################
issell = 0
try:
    def callback_method(message):
        #print(message)
        global df, df1, ltp, celtp, peltp, issell, cesold, pesold, stradle_premium, sold_stradle_premium, time_str, time_obj, time1_str, time1_obj, pnl, fig, ax1,ani, pldf, pldf1, t
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
        #time_str = message[19]
        # print("time_str = ", time_str)
        # print("type of time_str = ",type(time_str))
        df1 = pd.concat([df,df1])
        # time_obj = datetime.strptime(time_str, '%d/%m/%Y %H:%M:%S')
        # print("time_obj = ", time_obj)
        # print("type of time_obj = ", type(time_obj))
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
            pnl = sold_stradle_premium - stradle_premium
            print("P&L= Rs.", "%.2f" % (pnl*lot) )
            time1_str = df.iloc[-1]['null_19']
            time1_obj = datetime.strptime(time1_str, '%d/%m/%Y %H:%M:%S')
            t+= 1
            pldf = pd.DataFrame(data={'time':[t],'pnl':[pnl]})
            pldf1 = pd.concat([pldf,pldf1])
            pldf1.to_csv(r"pnl.txt", sep=',', mode='a', header = False, index = False)

            
        else:
            print("No TRADE")
        ########################################################
    client.subscribe(input_tokens=ws_token, callback=callback_method, broadcast_host="https://wstreamer.kotaksecurities.com/feed")

    # style.use('fivethirtyeight')

    # fig = plt.figure()
    # ax1 = fig.add_subplot(1,1,1)

    # def animate(i):
    #     graph_data = open('pnl.txt','r').read()
    #     lines = graph_data.split('\n')
    #     xs = []
    #     ys = []
    #     for line in lines:
    #         if len(line) > 1:
    #             x, y = line.split(',')
    #             xs.append(float(x))
    #             ys.append(float(y))
    #     ax1.clear()
    #     ax1.plot(xs, ys)
    # ani = animation.FuncAnimation(fig, animate, interval=1000)
    # plt.show()



except Exception as e:
    print("Exception when calling StreamingApi->subscribe: %s\n" % e)




#Unsubscribing to Streaming Websocket
# try:
#     # unsubscribe to the streamingAPI
#     client.unsubscribe()
# except Exception as e: 
#     print("Exception when calling StreamingApi->unsubscribe: %s\n" % e)
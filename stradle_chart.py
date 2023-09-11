from ks_api_client import ks_api
import os
from dotenv import load_dotenv
import pandas as pd
import time
from datetime import datetime
import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# from matplotlib import style
from matplotlib.animation import FuncAnimation

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
pldf1 = pd.DataFrame(data={'Time':[''],'Price':['']})

##############################################################################
x = list()
y = list()
###############################################################################
try:
    def callback_method(message):
        #print(message)
        global df, df1, ltp, celtp, peltp, stradle_premium, time_str, time_obj, ani, x , y, ct
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
        time_str = (df1.loc[(df1['opt_token'] == peinstrumentToken), 'null_19'].iloc[0])
        ct = datetime.strptime(time_str, '%d/%m/%Y %H:%M:%S')
        #ct = datetime.now().strftime("%H:%M:%S")
        stradle_premium = round((celtp + peltp),0)
        print(strike,"CE LTP = ", celtp)
        print(strike,"PE LTP = ", peltp)
        print("Stradle Premium = ", stradle_premium)
        ###################################################################################
        # time1_str = df.iloc[-1]['null_19']
        # time1_obj = datetime.strptime(time1_str, '%d/%m/%Y %H:%M:%S')
        # pldf = pd.DataFrame(data={'Time':[time1_str],'Price':[stradle_premium]})
        # pldf1 = pd.concat([pldf,pldf1])
        # pldf1.to_csv(r"stradle.csv", sep=',', mode='a', header = True, index = False)

        ########################################################
        x.append(ct)
        y.append(stradle_premium)
    client.subscribe(input_tokens=ws_token, callback=callback_method, broadcast_host="https://wstreamer.kotaksecurities.com/feed")


    plt.style.use('fivethirtyeight')

    def animate(i):
        plt.cla()
        plt.plot(x, y)


    ani = FuncAnimation(plt.gcf(), animate, 1000)


    plt.tight_layout()
    plt.show()





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
from ks_api_client import ks_api
import os
from dotenv import load_dotenv
import pandas as pd
import time
from colorama import Fore, Back, Style

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

cash = pd.read_csv ("ks_cash_scripmaster.txt",sep="|")
fno = pd.read_csv ("ks_fno_scripmaster.txt",sep="|")
expiry = os.getenv("banknifty_expiry")
instrumentName = 'BANKNIFTY'
underlying_name = 'NIFTY BANK'
max_opt_price = 9.5
lot = 25
strike_gap = 1200

############################################################################

underlying_token  = cash.loc[(cash['instrumentName'] == underlying_name) & (cash['instrumentType'] == 'IN') & (cash['segment'] == '-') & (cash['exchange'] == 'NSE'), 'instrumentToken'].iloc[0]
underlying_token  = int(underlying_token)
client.login(password = password)
client.session_2fa(access_code = otp)
quote_response = client.quote(instrument_token = underlying_token)
ltp = quote_response['success'][0]['ltp']
ltp = float(ltp)
atm = round(ltp/100)*100
protection_per = 3.5
upper_protection_per = 0.0
lower_protection_per = 0.0
i = 1
ceshort = atm
while ((upper_protection_per < protection_per) or (lower_protection_per < protection_per)) & (ceshort <= (atm+3000)):
    ceshort = atm + strike_gap
    peshort = atm - strike_gap
    celong = ceshort+100
    pelong = peshort-100
    #print(ceshort)
    #ceshort instrument tokens
    ceshorttoken = str(fno.loc[(fno['instrumentName'] == 'BANKNIFTY') & (fno['expiry'] == expiry) & (fno['optionType'] == 'CE') & (fno['strike'] == ceshort), 'instrumentToken'].iloc[0])
    ceshorttoken_int  = int(ceshorttoken)
    peshorttoken = str(fno.loc[(fno['instrumentName'] == 'BANKNIFTY') & (fno['expiry'] == expiry) & (fno['optionType'] == 'PE') & (fno['strike'] == peshort), 'instrumentToken'].iloc[0])
    peshorttoken_int  = int(peshorttoken)
    #otm1 instrument tokens
    celongtoken = str(fno.loc[(fno['instrumentName'] == 'BANKNIFTY') & (fno['expiry'] == expiry) & (fno['optionType'] == 'CE') & (fno['strike'] == celong), 'instrumentToken'].iloc[0])
    celongtoken_int  = int(celongtoken)
    pelongtoken = str(fno.loc[(fno['instrumentName'] == 'BANKNIFTY') & (fno['expiry'] == expiry) & (fno['optionType'] == 'PE') & (fno['strike'] == pelong), 'instrumentToken'].iloc[0])
    pelongtoken_int  = int(pelongtoken)
    #Getting Option Prices (ltp)
    ceceshort_quote_response = client.quote(instrument_token = ceshorttoken_int)
    peceshort_quote_response = client.quote(instrument_token = peshorttoken_int)
    celong_quote_response = client.quote(instrument_token = celongtoken_int)
    pelong_quote_response = client.quote(instrument_token = pelongtoken_int)
    ceceshortltp = float(ceceshort_quote_response['success'][0]['ltp'])
    peceshortltp = float(peceshort_quote_response['success'][0]['ltp'])
    celongltp = float(celong_quote_response['success'][0]['ltp'])
    pelongltp = float(pelong_quote_response['success'][0]['ltp'])
    #Calculating Upper Protection
    spread = ceceshortltp+peceshortltp-celongltp-pelongltp
    upper_protection = ceshort + spread
    lower_protection = peshort - spread
    upper_protection_per = ((upper_protection-ltp)/ltp)*100
    lower_protection_per = ((ltp-lower_protection)/ltp)*100
    strike_gap+= 100

    #printing Upper and Lower Protection
    print("--------------OTM ", i, " ----------------")
    print("Banknifty LTP = ", ltp)
    print(Fore.GREEN + "Buy ", celong, " CE LTP = ", celongltp)
    print(Style.RESET_ALL)
    print(Fore.RED + "Sell ", ceshort, " CE LTP = ", ceceshortltp)
    print(Style.RESET_ALL)
    print(Fore.RED + "Sell ", peshort, " PE LTP = ", peceshortltp)
    print(Style.RESET_ALL)
    print(Fore.GREEN + "Buy ", pelong, " PE LTP = ", pelongltp)
    print(Style.RESET_ALL)
    print("Preminum Received = ", "%.2f" % spread)
    print("Upper Protection = ", upper_protection, "%.2f" % upper_protection_per, "%")
    print("Lower Protection = ", lower_protection, "%.2f" % lower_protection_per, "%")
    # print("Upper Protection change Percentage = ", "%.2f" % upper_protection_per)
    # print("Lower Protection change Percentage = ", "%.2f" % lower_protection_per)
    if (upper_protection_per >= 1.3) & (lower_protection_per >= 1.3):
        print(Back.GREEN + "Good to Enrty")
        print(Style.RESET_ALL)
        print("Total Premium Received : ₹ ", "%.2f" % (spread*lot))
        callloss = (celong - upper_protection)
        putloss = (lower_protection - pelong)
        maxloss = max(callloss,putloss) * lot
        print("Max Loss = ₹ ", "%.2f" % maxloss )
        rr = maxloss/(spread*lot)
        print("Risk to Reward = ", rr)
    else:
        print("No to Enrty")
    i+= 1
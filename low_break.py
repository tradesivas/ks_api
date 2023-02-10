import pause, datetime
from datetime import date, time, datetime as dt
todays_date = date.today()
tdate = str(todays_date.year)+'-'+str(todays_date.month)+'-'+str(todays_date.day)
market_open = datetime.datetime(todays_date.year, todays_date.month, todays_date.day, 9, 5, 2, 0)
pause.until(market_open)
import tvDatafeed
import pandas as pd
import os
from colorama import Back, Style
from tvDatafeed import TvDatafeed,Interval
tv=TvDatafeed('sivaspeed856fa84b442b9245d2', 'vels8484')

c = (   time(9,0,2),time(9,5,2),time(9,10,2),time(9,15,2),time(9,20,2),time(9,25,2),time(9,30,2),time(9,35,2),time(9,40,2),time(9,45,2),time(9,50,2),time(9,55,2),
        time(10,0,2),time(10,5,2),time(10,10,2),time(10,15,2),time(10,20,2),time(10,25,2),time(10,30,2),time(10,35,2),time(10,40,2),time(10,45,2),time(10,50,2),time(10,55,2),
        time(11,0,2),time(11,5,2),time(11,10,2),time(11,15,2),time(11,20,2),time(11,25,2),time(11,30,2),time(11,35,2),time(11,40,2),time(11,45,2),time(11,50,2),time(11,55,2),
        time(12,0,2),time(12,5,2),time(12,10,2),time(12,15,2),time(12,20,2),time(12,25,2),time(12,30,2),time(12,35,2),time(12,40,2),time(12,45,2),time(12,50,2),time(12,55,2),
        time(13,0,2),time(13,5,2),time(13,10,2),time(13,15,2),time(13,20,2),time(13,25,2),time(13,30,2),time(13,35,2),time(13,40,2),time(13,45,2),time(13,50,2),time(13,55,2),
        time(14,0,2),time(14,5,2),time(14,10,2),time(14,15,2),time(14,20,2),time(14,25,2),time(14,30,2),time(14,35,2),time(14,40,2),time(14,45,2),time(14,50,2),time(14,55,2),
        time(15,0,2),time(15,5,2),time(15,10,2),time(15,15,2),time(15,20,2),time(15,25,2),time(15,30,2),time(15,35,2),time(15,40,2),time(15,45,2),time(15,50,2),time(15,55,2),
        time(16,0,2),time(16,5,2),time(16,10,2),time(16,15,2),time(16,20,2),time(16,25,2),time(16,30,2),time(16,35,2),time(16,40,2),time(16,45,2),time(16,50,2),time(16,55,2),
        time(17,0,2),time(17,5,2),time(17,10,2),time(17,15,2),time(17,20,2),time(17,25,2),time(17,30,2),time(17,35,2),time(17,40,2),time(17,45,2),time(17,50,2),time(17,55,2),
        time(18,0,2),time(18,5,2),time(18,10,2),time(18,15,2),time(18,20,2),time(18,25,2),time(18,30,2),time(18,35,2),time(18,40,2),time(18,45,2),time(18,50,2),time(18,55,2),
        time(19,0,2),time(19,5,2),time(19,10,2),time(19,15,2),time(19,20,2),time(19,25,2),time(19,30,2),time(19,35,2),time(19,40,2),time(19,45,2),time(19,50,2),time(19,55,2),
        time(20,0,2),time(20,5,2),time(20,10,2),time(20,15,2),time(20,20,2),time(20,25,2),time(20,30,2),time(20,35,2),time(20,40,2),time(20,45,2),time(20,50,2),time(20,55,2),
        time(21,0,2),time(21,5,2),time(21,10,2),time(21,15,2),time(21,20,2),time(21,25,2),time(21,30,2),time(21,35,2),time(21,40,2),time(21,45,2),time(21,50,2),time(21,55,2),
        time(22,0,2),time(22,5,2),time(22,10,2),time(22,15,2),time(22,20,2),time(22,25,2),time(22,30,2),time(22,35,2),time(22,40,2),time(22,45,2),time(22,50,2),time(22,55,2),
        time(23,0,2),time(23,5,2),time(23,10,2),time(23,15,2),time(23,20,2),time(23,25,2),time(23,30,2),time(23,35,2),time(23,40,2),time(23,45,2),time(23,50,2)
    )
j = 0
i = 0
now = dt.now()
current_time = now.time()
while j <= 179:
    if current_time <= c[j]:
        print("candle_value_taken is ",c[j])
        j = 180
    else:
        i+=1
        j+=1

print("      current_time is ", current_time)
print("                   i =", i)

candle_9_10 = datetime.datetime(todays_date.year, todays_date.month, todays_date.day, 9, 10, 2, 0)
pause.until(candle_9_10)
tenmin_data = tv.get_hist(symbol='SILVERMIC1!',exchange='MCX',interval=Interval.in_5_minute,n_bars=i)
high_9_00= tenmin_data.loc[tdate+' 09:00:00']['high']
high_9_05= tenmin_data.loc[tdate+' 09:05:00']['high']
print('high_9_00= ',high_9_00,'\n','high_9_05= ',high_9_05)
orbhigh = max(high_9_00,high_9_05)
print('10-min orb high is ', orbhigh)

h = (   {"h":9,"m":0},{"h":9,"m":5},{"h":9,"m":10},{"h":9,"m":15},{"h":9,"m":20},{"h":9,"m":25},{"h":9,"m":30},{"h":9,"m":35},{"h":9,"m":40},{"h":9,"m":45},{"h":9,"m":50},{"h":9,"m":55},
        {"h":10,"m":0},{"h":10,"m":5},{"h":10,"m":10},{"h":10,"m":15},{"h":10,"m":20},{"h":10,"m":25},{"h":10,"m":30},{"h":10,"m":35},{"h":10,"m":40},{"h":10,"m":45},{"h":10,"m":50},{"h":10,"m":55},
        {"h":11,"m":0},{"h":11,"m":5},{"h":11,"m":10},{"h":11,"m":15},{"h":11,"m":20},{"h":11,"m":25},{"h":11,"m":30},{"h":11,"m":35},{"h":11,"m":40},{"h":11,"m":45},{"h":11,"m":50},{"h":11,"m":55},
        {"h":12,"m":0},{"h":12,"m":5},{"h":12,"m":10},{"h":12,"m":15},{"h":12,"m":20},{"h":12,"m":25},{"h":12,"m":30},{"h":12,"m":35},{"h":12,"m":40},{"h":12,"m":45},{"h":12,"m":50},{"h":12,"m":55},
        {"h":13,"m":0},{"h":13,"m":5},{"h":13,"m":10},{"h":13,"m":15},{"h":13,"m":20},{"h":13,"m":25},{"h":13,"m":30},{"h":13,"m":35},{"h":13,"m":40},{"h":13,"m":45},{"h":13,"m":50},{"h":13,"m":55},
        {"h":14,"m":0},{"h":14,"m":5},{"h":14,"m":10},{"h":14,"m":15},{"h":14,"m":20},{"h":14,"m":25},{"h":14,"m":30},{"h":14,"m":35},{"h":14,"m":40},{"h":14,"m":45},{"h":14,"m":50},{"h":14,"m":55},
        {"h":15,"m":0},{"h":15,"m":5},{"h":15,"m":10},{"h":15,"m":15},{"h":15,"m":20},{"h":15,"m":25},{"h":15,"m":30},{"h":15,"m":35},{"h":15,"m":40},{"h":15,"m":45},{"h":15,"m":50},{"h":15,"m":55},
        {"h":16,"m":0},{"h":16,"m":5},{"h":16,"m":10},{"h":16,"m":15},{"h":16,"m":20},{"h":16,"m":25},{"h":16,"m":30},{"h":16,"m":35},{"h":16,"m":40},{"h":16,"m":45},{"h":16,"m":50},{"h":16,"m":55},
        {"h":17,"m":0},{"h":17,"m":5},{"h":17,"m":10},{"h":17,"m":15},{"h":17,"m":20},{"h":17,"m":25},{"h":17,"m":30},{"h":17,"m":35},{"h":17,"m":40},{"h":17,"m":45},{"h":17,"m":50},{"h":17,"m":55},
        {"h":18,"m":0},{"h":18,"m":5},{"h":18,"m":10},{"h":18,"m":15},{"h":18,"m":20},{"h":18,"m":25},{"h":18,"m":30},{"h":18,"m":35},{"h":18,"m":40},{"h":18,"m":45},{"h":18,"m":50},{"h":18,"m":55},
        {"h":19,"m":0},{"h":19,"m":5},{"h":19,"m":10},{"h":19,"m":15},{"h":19,"m":20},{"h":19,"m":25},{"h":19,"m":30},{"h":19,"m":35},{"h":19,"m":40},{"h":19,"m":45},{"h":19,"m":50},{"h":19,"m":55},
        {"h":20,"m":0},{"h":20,"m":5},{"h":20,"m":10},{"h":20,"m":15},{"h":20,"m":20},{"h":20,"m":25},{"h":20,"m":30},{"h":20,"m":35},{"h":20,"m":40},{"h":20,"m":45},{"h":20,"m":50},{"h":20,"m":55},
        {"h":21,"m":0},{"h":21,"m":5},{"h":21,"m":10},{"h":21,"m":15},{"h":21,"m":20},{"h":21,"m":25},{"h":21,"m":30},{"h":21,"m":35},{"h":21,"m":40},{"h":21,"m":45},{"h":21,"m":50},{"h":21,"m":55},
        {"h":22,"m":0},{"h":22,"m":5},{"h":22,"m":10},{"h":22,"m":15},{"h":22,"m":20},{"h":22,"m":25},{"h":22,"m":30},{"h":22,"m":35},{"h":22,"m":40},{"h":22,"m":45},{"h":22,"m":50},{"h":22,"m":55},
        {"h":23,"m":0},{"h":23,"m":5},{"h":23,"m":10},{"h":23,"m":15},{"h":23,"m":20},{"h":23,"m":25},{"h":23,"m":30},{"h":23,"m":35},{"h":23,"m":40},{"h":23,"m":45},{"h":23,"m":50}
    )
isbuy = False
isshort = False
isfirsttime = True

while i <= 179:
    next_candle = datetime.datetime(todays_date.year, todays_date.month, todays_date.day, h[i]['h'], h[i]['m'], 2, 0)
    print('waiting for '+str(h[i]['h'])+':'+str(h[i]['m'])+':2')
    pause.until(next_candle)
    next_data = tv.get_hist(symbol='SILVERMIC1!',exchange='MCX',interval=Interval.in_5_minute,n_bars=3)
    last_close = next_data.loc[tdate+' ' +str(h[i-1]['h'])+':'+str(h[i-1]['m'])+':00']['close']
    pre_close = next_data.loc[tdate+' ' +str(h[i-2]['h'])+':'+str(h[i-2]['m'])+':00']['close']
    pre_open = next_data.loc[tdate+' ' +str(h[i-2]['h'])+':'+str(h[i-2]['m'])+':00']['open']
    print(str(h[i-1]['h'])+':'+str(h[i-1]['m']),' close = ',last_close)
    print(str(h[i-2]['h'])+':'+str(h[i-2]['m']),' close = ',pre_close)
    print(str(h[i-2]['h'])+':'+str(h[i-2]['m']),' Open = ',pre_open)
    if pre_close <= orbhigh and last_close > orbhigh and isbuy == False:
        print('10-min orb high is ', orbhigh)
        print(Back.GREEN +'Buy entry Triggered at'+str(h[i]['h'])+':'+str(h[i]['m'])+':2')
        print(Style.RESET_ALL)
        isbuy = True
        buyat = str(h[i]['h'])+':'+str(h[i]['m'])+':2'
        if isfirsttime == True:
            print('Login to Kotaksec')
            isfirsttime = False
        
    elif isbuy == True and last_close < orbhigh:
        print('Alredy Bought at ', buyat)
        print(Back.RED +'Sell entry Triggered at'+str(h[i]['h'])+':'+str(h[i]['m'])+':2')
        print(Style.RESET_ALL)
        isbuy = False

    else:
        print(Back.YELLOW +'Buy entry NOT Triggered')
        print(Style.RESET_ALL)
    i+=1
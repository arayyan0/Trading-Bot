from collect import save_all_stocks
from analysis import momentum_analysis,from_online
from tracker import track_buys_sells,cull_stocks,plot_debt
import time
import datetime as dt
import numpy as np

#save_all_stocks()
#momentum_analysis()
#track_buys_sells('eqb.TO')
#cull_stocks()

def is_worktime():
    '''Checks if the current time aligns with regular trading times for the east coast'''
    now = dt.datetime.today()
    if now.date().weekday()<5 and dt.time(9,30) <= now.time() and \
    now.time() <= dt.time(16,30):
        return True
    else:
        return False
    
def run(): 
    
    if is_worktime():
        pass
    elif is_worktime()==False:
        #save_all_stocks()
        #momentum_analysis()
        #cull_stocks()
        
        with open('acceptable.txt') as f:
            content = f.readlines()
        acceptable = [x.strip() for x in content] 
        
        ticker = 'ECN.TO'
        max_buy = 96
        max_sell = 110
        
        plot_debt(ticker=ticker,max_buy=max_buy,max_sell=max_sell)
        
run()
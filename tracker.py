from analysis import momentum_check
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

def track_buys_sells(ticker='CSU.TO'):
    
    date,buy_or_sell,buy,sell = momentum_check(ticker,date_track=True,max_buy=96,max_sell=108)
    sell_counter=0
    buy_counter=0
    
    for i in range(0,len(date)):
        
        if buy_or_sell[i]=='buy':
            print('Buy on  {}  for  {}'.format(date[i],buy[buy_counter]))
            buy_counter+=1
        else:
            print('Sell on  {}  for  {}'.format(date[i],sell[sell_counter]))
            sell_counter+=1
            
def cull_stocks():
    
    df = pd.read_csv('analysis_results.csv')

    if os.path.isfile('acceptable.txt'):
        os.remove('acceptable.txt')
    
    culled_stocks = []
    
    for index,row in df.iterrows():
        if float(row['Return/Price'])>2:
            culled_stocks.append(str(row['Ticker']))
            
    np.savetxt('acceptable.txt',np.array(culled_stocks),fmt='%s')
    
def plot_debt(ticker='CSU.TO',max_buy=96,max_sell=108):
    
    date,buy_or_sell,buy,sell = momentum_check(ticker,date_track=True,max_buy=max_buy,max_sell=max_sell)
    
    total = np.zeros(len(buy_or_sell))
    tot=0
    buy_index=0
    sell_index=0
    
    for i in np.arange(0,len(total)):
        if buy_or_sell[i]=='buy':
            total[i]=-buy[buy_index]+tot
            tot-=buy[buy_index]
            buy_index+=1
        else:
            total[i]=sell[sell_index]+tot
            tot+=sell[sell_index]
            sell_index+=1
            
    plt.plot(date,total)
    plt.title(ticker)
    
    ax = plt.gca()
    ax.set_xticks([0,int(len(total)/3),2*int(len(total)/3),len(total)])
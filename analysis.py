from gather_exchange_tickers import save_sp500_tickers, save_tsx
from collect import get_info
import numpy as np
import pandas as pd
import os
import time

def momentum_check(ticker='CSU.TO',max_buy=95,max_sell=105,date_track=False):
    '''Called by momentum analysis to do the heavy lifting'''
    #print('Starting {}'.format(ticker))
    try:
        if str(ticker[-3:])=='.TO':
            ticker=ticker[:-3]
    except TypeError:
        return [],[]
    
    data = pd.read_csv('../Collected_Data/Close/{}.csv'.format(ticker))
    
    date = []
    buy_or_sell = []
    buy = []
    sell = []
    
    trading_cost=5
    number_of_shares_bought = 10
    
    for index,row in data.iterrows():
        
        if row['Momentum']<=max_buy:
            if data.iloc[index-1]['Momentum']<=max_buy+1:
                if data.iloc[index-1]['Momentum']<=max_buy+1:
                    buy.append(row['Adj Close']+trading_cost/\
                               number_of_shares_bought)
                    date.append(row['Date'])
                    buy_or_sell.append('buy')
                    #print('buying at {}'.format(row['Adj Close']))
                    
        if row['Momentum']>=max_sell:
            if data.iloc[index-1]['Momentum']>=max_sell+1:
                if len(sell)!=len(buy):
                    count=0
                    for i in np.arange(len(buy)-len(sell)):
                        if count==0:
                            sell.append(row['Adj Close']-trading_cost/\
                                        number_of_shares_bought)
                        else:
                            sell.append(row['Adj Close'])
                        date.append(row['Date'])
                        buy_or_sell.append('sell')
                        count+=1
                        #print('selling at {}'.format(row['Adj Close']))

    if date_track:
        return date,buy_or_sell,buy,sell
    else:
        return buy,sell        
        
def from_online(ticker='CSU.TO'):
    '''Getting extra information for a specific stock'''
    stuff = get_info(ticker)
    
    PE = [stuff['trailingPE'],stuff['forwardPE']]
    EP = [stuff['epsTrailingTwelveMonths'],stuff['epsForward']]
    
    PE_ratio = abs(PE[0]+PE[1])/2
    PE_growth = PE[0]-PE[1]
    EPS = abs(EP[0]+EP[1])/2
    
    market_cap = stuff['marketCap']

    #print(stuff,'\n',PE_ratio,'\n',PE_growth,'\n',EPS,'\n',market_cap/1000000)
    return PE_ratio,PE_growth,EPS,market_cap/1000000000

def get_money(result,ticker):
    
    
    df = pd.DataFrame({'Ticker':[ticker],'Result':[result]})
    
    df.to_csv('analysis_results.csv', mode='a', header=False)
    
def momentum_analysis():
    '''The first analysis method that is saved as an excel file'''
    stocks = save_tsx()
    print(stocks)
    #stocks = save_sp500_tickers()+save_tsx()
    
    if os.path.isfile('analysis_results.csv'):
        os.remove('analysis_results.csv')
    
    buy_list = [90,92,94,96]
    sell_list = [110,108,106,104]
    
    mast = {}
    
    for i in stocks:
        
        for j in buy_list:
            for k in sell_list:
                try:
                    buy,sell = momentum_check(i,j,k)
                except KeyError:
                    break
                if buy==[] and sell ==[]:
                    continue
                result = np.sum(sell)-np.sum(buy[:len(sell)])
                mast['{}-{}'.format(j,k)]=result
            else:
                continue
            break
        if buy==[] and sell==[]:
            continue
        df = pd.DataFrame({'Ticker':[i]})
        for k,j in mast.items():
            df[k]=j
        ticker = i
        if i[-3:]=='.TO':
            i=i[:-3]
        close = pd.read_csv('../Collected_Data/Close/{}.csv'.format(i))
        df['Price']=close.iloc[-1]['Adj Close']
        df['Return/Price']=df.max(axis=1)/df['Price']
        try:
            PE_Ratio,PE_growth,EPS,Market_Cap = from_online(ticker)
        except:
            PE_Ratio='NA'
            PE_growth='NA'
            EPS='NA'
            Market_Cap='NA' 
        df['EPS']=EPS
        df['P/E Ratio']=PE_Ratio
        df['P/E growth']=PE_growth
        df['Market Cap (Bil)']=Market_Cap
        
        if os.path.isfile('analysis_results.csv'):
            df.to_csv('analysis_results.csv', mode='a', header=False)
        else:
            df.to_csv('analysis_results.csv', header=True)
            
        time.sleep(5)
        print('done with {}'.format(i))
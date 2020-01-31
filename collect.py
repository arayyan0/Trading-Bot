import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def collect_data(ticker='CSU.TO',intraday=False):
    '''Compiles all the information wanted to be saved as a csv'''
    
    if intraday:
        data = yf.download(tickers=ticker,period='1mo',interval='15m')
    else:
        data = yf.download(tickers=ticker,period='3y',interval='1d')
        
    data = momentum(data)
    
    if ticker[-3:]=='.TO' and intraday==True:
        data.to_csv('../Collected_Data/Intraday/{}.csv'.format(ticker[:-3]))
    elif intraday==True:
        data.to_csv('../Collected_Data/Intraday/{}.csv'.format(ticker))
    elif ticker[-3:]=='.TO' and intraday==False:
        data.to_csv('../Collected_Data/Close/{}.csv'.format(ticker[:-3]))
    else:
        data.to_csv('../Collected_Data/Close/{}.csv'.format(ticker))
    
def instantaneous_info(ticker='CSU.TO'):
    
    stock = yf.Ticker(ticker)
    
    return stock.get_info()
    
def momentum(data):
    
    momentum = [0,0,0,0,0]
    count=0
    
    for index,row in data.iterrows():
        
        if count<5:
            count+=1
            continue
        
        quantity = data.iloc[count]['Adj Close']/data.iloc[count-5]['Adj Close']

        momentum.append(quantity*100)
        
        count+=1
        
    data['Momentum']=momentum
    
    return data
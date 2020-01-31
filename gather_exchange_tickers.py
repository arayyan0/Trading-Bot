import pickle
import bs4 as bs
import requests
import pandas as pd

def save_tsx():
    '''Basically copy pasted save_sp500_tickers'''
    
    df = pd.read_csv('tsx_tickers.csv')
    
    stock_names = df['Symbol']+str('.TO')
    
    return list(stock_names)

def save_sp500_tickers():
    
    '''This function takes the S&P 500 list'''
    
    df = pd.read_csv('sp-500.csv')
    
    stock_names = df['Symbol']
    
    return list(stock_names)
import yfinance as yf
import numpy as np
import pandas as pd
import requests
import bs4 as bs

def momentum_check(ticker='CSU',max_buy=95,max_sell=105):
    
    #print('Starting {}'.format(ticker))
    try:
        if str(ticker[-3:])=='.TO':
            ticker=ticker[:-3]
    except TypeError:
        return [],[]
    
    data = pd.read_csv('../Collected_Data/Close/{}.csv'.format(ticker))
    
    buy = []
    sell=[]
    
    trading_cost=5
    number_of_shares_bought = 1
    
    for index,row in data.iterrows():
        
        if row['Momentum']<=max_buy:
            if data.iloc[index-1]['Momentum']<=max_buy+1:
                if data.iloc[index-1]['Momentum']<=max_buy+1:
                    buy.append(row['Adj Close']+trading_cost/\
                               number_of_shares_bought)
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
                        count+=1
                        #print('selling at {}'.format(row['Adj Close']))

    return buy,sell


def valuation(ticker='CSU.TO'):
    
    stock = yf.Ticker(ticker).get_info()
    expected_PE_increase = False
    
    eps_ratio = stock['forwardEps']/stock['trailingEps']
    pe_ratio = stock['forwardPE']/stock['trailingPE']
    
    if pe_ratio>1:
        expected_PE_increase = True
    
    if eps_ratio>pe_ratio:
        print('Earnings do better than PE')
        print(eps_ratio,pe_ratio**-1)
        
        
def from_marketwatch(ticker='CSU.TO'):
    
    '''Takes certain quantities about the current stock from marketwatch'''
    
    country='us'
    if ticker[-3:]=='.TO':
        country='ca'
        ticker=ticker[:-3]
    
    if country=='ca':
        resp=requests.get('https://www.marketwatch.com/investing/stock/{}?countrycode=ca'.format(ticker))
    else:
        resp=requests.get('https://www.marketwatch.com/investing/stock/{}'.format(ticker))
    soup = bs.BeautifulSoup(resp.text,'lxml')
    table = soup.find('ul',{'class':'list list--kv list--col50'})
    EPS = 0
    PE_Ratio=0
    Market_Cap=0
    
    try:
        table.findAll('li')
    except:
        return 'N/A','N/A','N/A'
    
    for row in table.findAll('li'):
        for foo in row.findAll('small'):
            if str(foo)=='<small class="kv__label">EPS</small>':
                eps = row.findAll('span')
            elif str(foo)=='<small class="kv__label">P/E Ratio</small>':
                pe_ratio = row.findAll('span')
            elif str(foo)=='<small class="kv__label">Market Cap</small>':
                market_cap = row.findAll('span')
                
    try:
        EPS = float(str(eps[0])[38:-7])
    except ValueError:
        EPS = 0
    try:
        PE_Ratio = float(str(pe_ratio[0])[37:-7])
    except ValueError:
        PE_Ratio=0
    try:
        Market_Cap = float(str(market_cap[0])[38:-8])
    except ValueError:
        Market_Cap=0
        
    return EPS, PE_Ratio, Market_Cap
                    
def get_money(result,ticker):
    
    
    df = pd.DataFrame({'Ticker':[ticker],'Result':[result]})
    
    df.to_csv('analysis_results.csv', mode='a', header=False)
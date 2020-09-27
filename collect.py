from gather_exchange_tickers import save_sp500_tickers, save_tsx
import yfinance as yf
import os
import fnmatch

def collect_data(ticker='CSU.TO',intraday=False):
    '''Compiles all the information wanted to be saved as a csv'''
    
    if ticker[-3:]=='.TO':
        pos = ticker[:-3].find('.',0,-1)
        if pos!=-1:
            ticker = ticker.replace('.','-',1)
        print(ticker)
    else:
        pos = ticker.find('.',0,-1)
        if pos!=-1:
            ticker = ticker.replace('.','-',1)
        print(ticker)
        
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
    
def get_info(ticker='CSU.TO'):
    
    stock = yf.Ticker(ticker)
    
    return stock.info
    
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

def save_all_stocks():
    
    if not os.path.exists('../Collected_Data/Intraday/'):
        os.makedirs('../Collected_Data/Intraday/')
        
    if not os.path.exists('../Collected_Data/Close/'):
        os.makedirs('../Collected_Data/Close/')
    
    #stocks = save_sp500_tickers()+save_tsx()
    stocks = save_tsx()
    print(stocks)
    for i in stocks:
        
        try:
            collect_data(i)
        except:
            continue
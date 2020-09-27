import pandas as pd

def save_tsx():
    '''Basically copy pasted save_sp500_tickers'''
    
    df = pd.read_csv('tsx_tickers.csv')
    df = df.dropna()
    
    stock_list = []
    for index,row in df.iterrows():
        if '.' in str(row['Symbol']):
            row['Symbol'] = str(row['Symbol']).replace('.','-')
        stock_list.append(str(row['Symbol'])+str('.TO'))
    
    return stock_list

def save_sp500_tickers():
    
    '''This function takes the S&P 500 list'''
    
    df = pd.read_csv('sp-500.csv')
    
    stock_names = df['Symbol']
    
    return list(stock_names)
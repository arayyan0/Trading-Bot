import numpy as np
import pandas as pd

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
    
    for index,row in data.iterrows():
        
        if row['Momentum']<=max_buy:
            if data.iloc[index-1]['Momentum']<=max_buy+1:
                if data.iloc[index-1]['Momentum']<=max_buy+1:
                    buy.append(row['Adj Close'])
                    #print('buying at {}'.format(row['Adj Close']))
                    
        if row['Momentum']>=max_sell:
            if data.iloc[index-1]['Momentum']>=max_sell+1:
                if len(sell)!=len(buy):
                    for i in np.arange(len(buy)-len(sell)):
                        sell.append(row['Adj Close'])
                        #print('selling at {}'.format(row['Adj Close']))
                        
    return buy,sell
                    
def get_money(result,ticker):
    
    
    df = pd.DataFrame({'Ticker':[ticker],'Result':[result]})
    
    df.to_csv('analysis_results.csv', mode='a', header=False)
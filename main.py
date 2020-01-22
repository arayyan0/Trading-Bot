from collect import *
from analysis import *
from gather_exchange_tickers import *
import csv
import os

def plot():
    #collect_data(intraday=False)
    stuff = pd.read_csv('../Collected_Data/Close/CSU.csv')
    
    fig = plt.figure(figsize=[18,12])
    
    plt.plot(stuff['Date'],stuff['Momentum'])
    #plt.plot(100*np.ones(len(stuff['Date'])),stuff['Date'])
    
    ax=plt.gca()
    ax.set_ylim(85,120)
    ax.set_xlim(2300,2510)
    
def print_info(ticker='CSU'):
    
    try:
        momentum_check(ticker)
    except FileNotFoundError:
        collect_data(ticker)
        momentum_check(ticker)
    
def save_all_stocks():
    
    #stocks = save_sp500_tickers()+save_tsx()
    stocks = save_tsx()
    print(stocks)
    for i in stocks:
        try:
            collect_data(i)
        except:
            continue
 
def momentum_analysis():
    
    stocks = save_tsx()
    
    if os.path.isfile('analysis_results.csv'):
        os.remove('analysis_resuslts.csv')
    
    buy_list = [90,92,94,96]
    sell_list = [110,108,106,104]
    
    mast = {}
    
    for i in stocks:
        
        for j in buy_list:
            for k in sell_list:
                buy,sell = momentum_check(i,j,k)
                if buy==[] and sell ==[]:
                    continue
                result = np.sum(sell)-np.sum(buy[:len(sell)])
                mast['{}-{}'.format(j,k)]=result
                
# =============================================================================
#         get_money([mast['90110'],mast['90108'],mast['90106'],mast['90104'],\
#                    mast['92110'],mast['92108'],mast['92106'],mast['92104'],\
#                    mast['94110'],mast['v94108'],mast['94106'],mast['94104'],\
#                    mast['96110'],mast['96108'],mast['96106'],mast['96104']],i)
# =============================================================================
        if buy==[] and sell==[]:
            continue
        df = pd.DataFrame({'Ticker':[i]})
        for k,j in mast.items():
            df[k]=j
        if i[-3:]=='.TO':
            i=i[:-3]
        close = pd.read_csv('../Collected_Data/Close/{}.csv'.format(i))
        df['Price']=close.iloc[-1]['Adj Close']
        df['Return/Price']=df['96-108']/df['Price']
        
        if os.path.isfile('analysis_results.csv'):
            df.to_csv('analysis_results.csv', mode='a', header=False)
        else:
            df.to_csv('analysis_results.csv', header=True)
    
        print('done with {}'.format(i))
    
#print_info('CSU.TO')    
#save_all_stocks()
#save_all_stocks()
momentum_analysis()
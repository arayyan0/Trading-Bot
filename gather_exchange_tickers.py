import pickle
import bs4 as bs
import requests

def save_tsx():
    '''Basically copy pasted save_sp500_tickers and changed the url'''
    
    resp=requests.get('https://en.wikipedia.org/wiki/S%26P/TSX_Composite_Index')
    soup = bs.BeautifulSoup(resp.text,'lxml')
    table = soup.find('table',{'class':'wikitable sortable'})
    stock_names = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text+str('.TO')
        stock_names.append('{}'.format(ticker))
            
    with open('tsxtickers.pickle','wb') as f:
        pickle.dump(stock_names,f)
    
    return stock_names

def save_sp500_tickers():
    
    '''This function takes the S&P 500 list and creates csvs for each of them
    using beautiful soup'''
    
    resp=requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text,'lxml')
    table = soup.find('table',{'class':'wikitable sortable'})
    stock_names = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text[:-1]
        stock_names.append(ticker)
            
    with open('sp500tickers.pickle','wb') as f:
        pickle.dump(stock_names,f)
    
    return stock_names
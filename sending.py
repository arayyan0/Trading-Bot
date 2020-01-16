from questrade_api import Questrade
q = Questrade(refresh_token="sTjfVl99dEjS6M9vACjE4C7TuiVS7ElE0")
#q = Questrade()

print(q.markets_quote(34658))   

#import requests
#response = requests.get("https://api05.iq.questrade.com/")
#print(response)
from questrade_api import Questrade
import numpy as np

token = np.loadtxt('../token.txt')
print(token)
q = Questrade(refresh_token=token)

print(q.markets_quote(34658))
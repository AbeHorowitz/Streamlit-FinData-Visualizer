import pyEX as p
import requests
import numpy as np

c = p.Client(api_token='Tpk_057363474545412b9a53956f425fa12d', version='sandbox') #using Sandbox API token so not counting against monthly limit

df = c.chartDF(symbol='TSLA', timeframe='6m')[['close', 'volume']] #get DataFrame

print("Initial: ")
print(df)

params = {'ticker':'TSLA', 'from_datetime':'2021:11:11:08:30:00', 'until_datetime':'2021:11:16:08:30:00', 'agg_mode':'D'}

initial = requests.get('Secret Proprietary API Link', params=params).json() # Non-publishable API link with access to a proprietary statistic developed by my employer

print("Prop Stat JSON:")
print(initial)

stat = np.array([]) # stat is the secret statistic

for i in initial:
	for j in i.values():
		stat = np.append(stat, j)

print("Prop Stat Array:")
print(stat)

df['New Thing'] = stat

print(df)

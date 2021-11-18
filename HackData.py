import pyEX as p
import requests
import numpy as np

c = p.Client(api_token='Tpk_057363474545412b9a53956f425fa12d', version='sandbox') #using Sandbox API token so not counting against monthly limit

df = c.chartDF(symbol='TSLA', timeframe='6m')[['close', 'volume']] #get DataFrame

print("Initial: ")
print(df)

params = {'ticker':'TSLA', 'from_datetime':'2021:11:11:08:30:00', 'until_datetime':'2021:11:16:08:30:00', 'agg_mode':'D'}

initial = requests.get('http://mars.larium.ai:8002/tweets/get_pulse', params=params).json()

print("Pulse JSON:")
print(initial)

pulse = np.array([])

for i in initial:
	for j in i.values():
		pulse = np.append(pulse, j)

print("Pulse Array:")
print(pulse)

df['New Thing'] = pulse

print(df)
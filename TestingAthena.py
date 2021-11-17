"""
What this showed was that the bounds of Athena in the D mode is 209 data points, since, as we found before,
when ending at the date of November 16, it could not call data from before April 17.

It also showed that the function is inclusive of both end-bounds (beginning date and end date) included in parameters.
"""

import requests

params = {'ticker':'AAPL', 'from_datetime':'2021:04:18:00:00:00', 'until_datetime':'2021:11:11:16:00:00', 'agg_mode':'D'}
params2 = {'ticker':'AAPL', 'from_datetime':'2021:04:16:00:00:00', 'until_datetime':'2021:11:11:16:00:00', 'agg_mode':'D'}

data_trial = requests.get('non-publishable Athena API link', params=params)
data_trial2 = requests.get('non-publishable Athena API link', params=params2)

print("Part 1: The Set Starting on April 18")
print("\nInitial Status Code: ")
print(data_trial.status_code)

print("\nActual JSON File: ") 
print(data_trial.json())

print("\nLength of JSON:")
print(len(data_trial.json()))

print("----------------------------------------")

print("Part 2: The Set Starting on April 16")

print("\nInitial Status Code: ")
print(data_trial2.status_code)

print("\nActual JSON File: ") 
print(data_trial2.json())

print("\nLength of JSON:")
print(len(data_trial2.json()))
import pyEX as p
import requests
import numpy as np

from datetime import date
from datetime import timedelta
from datetime import datetime
from dateutil.easter import easter
import holidays

c = p.Client(api_token='Tpk_057363474545412b9a53956f425fa12d', version='sandbox') #using Sandbox API token so not counting against monthly limit

def get_data(symbol, start_date, end_date): # Inclusive on both upper/lower bounds
	# 1) Get Stock info
	# 1a) An unfortunately necessary pre-req: While Secret API is inclusive on both bounds, pyEX is exclusive on lower bound.
	# Begin by correcting this in all cases, as need be. '2021-05-25'
	temp = datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=-1)
	df_start_date = temp.strftime('%Y-%m-%d')

	df = c.chartDF(symbol='TSLA', timeframe='1y')[['close', 'volume']].loc[df_start_date:end_date]

	#2) Convert OG date to date good for secret_stat API/Streamlit.date_input returns a date in ISO 8601 format of year-month-day such as 2021-11-02
	year1, year2 = start_date[:4], end_date[:4] # These variables will be used again later
	s, e = [year1, start_date[5:7], start_date[8:]], [year2, end_date[5:7], end_date[8:]]
	start, end = "", ""
	for i in s: start += i+":"
	for i in e: end += i+":"

	#3) get data
	params = {'ticker': symbol, 'from_datetime': start+'08:30:00', 'until_datetime' : end+'08:30:00', 'agg_mode':'D'}
	secret_stat_init = requests.get('Secret API Link', params=params).json()
	
	#4) match up secret_stat data indices with DataFrame date indices
	secret_stat, secret_stat_time = np.array([]), []
	holidays1, holidays2 = createHolidayCalendar(year1), None
	if year1!=year2: holidays2 = createHolidayCalendar(year2)# If necessary, also set up year2 holidays for the second year

	#run isValidTradingDay depending on which year. More efficient: set up
	#isValidTrading Day to take in isodate, a dictionary with holiday calendars. Depending on year in isodate,
	#use one of the holiday calendars.
	#OR, just redo this piece to use the Pandas library instead: https://stackoverflow.com/questions/2394235/detecting-a-us-holiday
	for i in secret_stat_init:
		for j in i.keys():
			if j[:4]==year1:
				if isValidTradingDay(j[:10], holidays1):
					secret_stat_time.append(j)
					secret_stat = np.append(secret_stat, i[j])
			elif j[:4]==year2:
				if isValidTradingDay(j[:10], holidays2):
					secret_stat_time.append(j)
					secret_stat = np.append(secret_stat, i[j])

	# 5) Finish: If the datasets matchup, write the dataframe to a file to be used elsewhere, to avoid overcalling Athena API 
	# If the datasets don't matchup, then inform developer to correct error.
	try: 
		df['secret_stat'] = secret_stat
		df.reset_index(inplace=True)
		df.to_pickle("TeslaDFActual.pkl")
	except ValueError:
		for i in secret_stat_time:
			if i[:10] not in [i.strftime('%Y-%m-%d') for i in df.index]:
				print("The following date was included in the secret_stat dataset but not included in the equity data. Please review isValidTradingDay method:", i)

def isValidTradingDay(isodate, holidays):
	day = date.fromisoformat(isodate).isoweekday()
	status = holidays.get(isodate)
	if day==6 or day==7 or status!= None:
		return(False)
	else:
		return(True)


# Select country
def createHolidayCalendar(year):
	us_holidays = holidays.US(years=int(year))
	us_holidays.pop_named('Veterans Day')
	us_holidays.pop_named('Columbus Day')
	try:
		us_holidays.pop_named('Veterans Day (Observed)')
	except KeyError:
		pass
	try:
		us_holidays.pop_named('Columbus Day (Observed)')
	except KeyError:
		pass

	good_friday = easter(int(year)) + timedelta(days=-2)

	us_holidays.append({good_friday:'Good Friday'})

	return(us_holidays)

get_data('TSLA', '2021-05-10', '2021-10-15')


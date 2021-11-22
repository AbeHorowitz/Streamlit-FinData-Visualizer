import pyEX as p
import requests
import numpy as np

from datetime import date
from datetime import timedelta
import dateutil.easter
import holidays

c = p.Client(api_token='Tpk_057363474545412b9a53956f425fa12d', version='sandbox') #using Sandbox API token so not counting against monthly limit

def get_data(symbol, start_date, end_date):
	
	df = c.chartDF(symbol='TSLA', timeframe='1y')[['close', 'volume']].loc[start_date:end_date]
	year_1 = start_date[:4] #these variables will be used again later
	year_2 = end_date[:4]
	#Streamlit.date_input returns a date in ISO 8601 format of year-month-day such as 2021-11-02
	s = [year_1, start_date[5:7], start_date[8:]]
	e = [year_2, end_date[5:7], end_date[8:]]

	start = ""
	end = ""
	
	for i in s:
		start += i+":"
	for i in e:
		end += i+":"

	params = {'ticker': symbol, 'from_datetime': start+'08:30:00', 'until_datetime' : end+'08:30:00', 'agg_mode':'D'}

	stat_init = requests.get('secret API link', params=params).json() #in the real code, there is a proprietary, non-publishable statistic here
	stat = np.array([])
	stat_time = []

	holidays = createHolidayCalendar('year1')

	for i in pulse_init:
		for j in i.keys():
			if isValidTradingDay(j[:10], holidays):
				stat_time.append(j)
				pulse = np.append(stat, i[j])

	df['Secret Proprietary Statistic'] = stat

	df.reset_index(inplace=True)


	print(df)

def isValidTradingDay(isodate, holidays):
	day = date.fromisoformat(isodate).isoweekday()
	status = holidays.get(isodate)
	if day==6 or day==7 or status!= None:
		return(False)
	else:
		return(True)


# Select country
def createHolidayCalendar(year):
	year = float(year)
	us_holidays = holidays.US(years=year)
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

	good_friday = dateutil.easter.easter(year) + timedelta(days=-2)

	us_holidays.append({good_friday:'Good Friday'})

	return(us_holidays)

get_data('TSLA', '2021-10-10', '2021-10-21')


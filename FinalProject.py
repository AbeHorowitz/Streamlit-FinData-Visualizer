import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import streamlit as st

import pyEX as p
import requests
import numpy as np

from datetime import date
from datetime import timedelta
from datetime import datetime
from dateutil.easter import easter
import holidays

c = p.Client(api_token='sk_a2d39f374ea044fbb6c7127976961748', version='stable') #using Sandbox API token so not counting against monthly limit

class Visualizer:
	def __init__(self, symbol, start_date, end_date):
		self.symbol = symbol
		self.start_date = end_date
		self.end_date = end_date

	def get_data(self): # Inclusive on both upper/lower bounds
		# Athena is inclusive on both bounds, but pyEX is exclusive on lower bound. Correct in all cases.
		temp = datetime.strptime(self.start_date, '%Y-%m-%d') + timedelta(days=-1)
		df_start_date = temp.strftime('%Y-%m-%d')

		self.df = c.chartDF(symbol='TSLA', timeframe='1y')[['close', 'volume']].loc[df_start_date:end_date]

		start = self.isotoAPI(self.start_date)
		end = self.isotoAPI(self.end_date)

		self.secret_stat = self.Secret_Stat()
		# 5) Finish: If the datasets matchup, write the dataframe to a file to be used elsewhere, to avoid overcalling Athena API 
		# If the datasets don't matchup, then inform developer to correct error.
		try: 
			df['secret_stat'] = secret_stat
			df.reset_index(inplace=True)
			self.time = self.df.iloc[:,0].values
		except ValueError:
			for i in secret_stat_time:
				if i[:10] not in [i.strftime('%Y-%m-%d') for i in df.index]:
					print("The following date was included in the secret_stat dataset but not included in the equity data. Please review isValidTradingDay method:", i)
		return(self)

	@classmethod				
	def Secret_Stat(self):
		secret_stat_init = self.getSecret_Stat(symbol, start, end, agg='D')
		
		# Match up secret_stat data indices with DataFrame date indices
		secret_stat, secret_stat_time = np.array([]), []
		holidays1, holidays2 = self.createHolidayCalendar(year1), None
		if year1!=year2: holidays2 = createHolidayCalendar(year2)# If necessary, also set up year2 holidays for the second year

		for i in secret_stat_init:
			for j in i.keys():
				if j[:4]==year1:
					if self.isValidTradingDay(j[:10], holidays1):
						secret_stat_time.append(j)
						secret_stat = np.append(secret_stat, i[j])
				elif j[:4]==year2:
					if self.isValidTradingDay(j[:10], holidays2):
						secret_stat_time.append(j)
						secret_stat = np.append(secret_stat, i[j])

		return(self)

	@staticmethod # Raw secret_stat data from API
	def getsecret_stat(symbol, start, end, agg):
		parameters = {'ticker': symbol, 'from_datetime': start+'08:30:00', 'until_datetime' : end+'08:30:00', 'agg_mode': agg}
		return(requests.get('Secret API Request', params=params).json())

	"""
	Next Two Methods: Convert OG date to date good for secret_stat API/Streamlit.date_input returns a date in ISO 8601 
	format of year-month-day such as 2021-11-02
	"""
	@staticmethod
	def isotoAPI(isodate):
		year = yearISO(isodate)
		array, result = [year, isodate[5:7], isodate[8:]], ""
		for part in array: result += i+":"
		return(result)

	@staticmethod
	def yearISO(isodate):
		return isodate[:4]

# Valid trading day boolean: False if weekend or trading holiday
	@staticmethod 
	def isValidTradingDay(isodate, holidays):
		day = date.fromisoformat(isodate).isoweekday()
		status = holidays.get(isodate)
		if day==6 or day==7 or status!= None:
			return(False)
		else:
			return(True)


# Create list of trading holidays in US, to filter out datapoints from secret_stat API
	@staticmethod
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

	@classmethod
	def twoSubplots(self):
		self.fig = make_subplots(rows=1, cols=2, subplot_titles=(
			f'Daily Price of {self.symbol}', 
			f'Daily secret_stat of {self.symbol}'))
		self.fig.add_trace(
			go.Scatter(x=time, y=close),
			row=1, col=1)

		self.fig.add_trace(
			go.Scatter(x=time, y=secret_stat),
			row=1, col=2)

		self.fig['layout']['xaxis']['title']='Time'
		self.fig['layout']['xaxis2']['title']='Time'
		self.fig['layout']['yaxis']['title']='Daily Close Price'
		self.fig['layout']['yaxis2']['title']='Daily secret_stat'

		return self.fig

	@classmethod
	def secondaryY(self):
		self.fig = make_subplots(specs=[[{"secondary_y": True}]])

		self.fig.add_trace(
			go.Scatter(x=self.time, y=self.volume, name="Volume"),
			secondary_y=False,
		)

		self.fig.add_trace(
			go.Scatter(x=self.time, y=self.secret_stat, name="Secret_Stat"),
			secondary_y=True,
		)

		# Add figure title
		self.fig.update_layout(
			title_text="Volume vs. Secret_Stat"
		)

			# Set x-axis title
		self.fig.update_xaxes(title_text="Time")

			# Set y-axes titles
		self.fig.update_yaxes(title_text="Volume", secondary_y=False)
		self.fig.update_yaxes(title_text="Secret_Stat Data", secondary_y=True)

		return self.fig

	@classmethod
	def streamRun(self):
		self.secondaryY()
		st.plotly_chart(self.fig)

visual = Visualizer(st.selectbox("Ticker", ["TSLA", "AAPL"]), st.date_input("Start"), st.date_input("End"))
visual.streamRun()



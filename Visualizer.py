import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import streamlit as st

import pyEX as p
import requests
import numpy as np

from datetime import date, timedelta, datetime
from dateutil.easter import easter
import holidays

c = p.Client(api_token='sk_a2d39f374ea044fbb6c7127976961748', version='stable') #using Sandbox API token so not counting against monthly limit

class Visualizer:
	def __init__(self, symbol, start_date, end_date):
		self.symbol = symbol
		self.start_date = start_date
		self.end_date = end_date

	# (1) DATA
	def getData(self):
		# Athena is inclusive on both bounds, but pyEX is exclusive on lower bound. Correct in all cases.
		temp = self.start_date + timedelta(days=-1)
		df_start_date = temp.strftime('%Y-%m-%d')
		df_end_date = self.end_date.strftime('%Y-%m-%d')
		df = c.chartDF(symbol=self.symbol, timeframe='1y')[['close', 'volume']].loc[df_start_date:df_end_date]
		df.reset_index(inplace=True)
		return df

	def createPulse(self):
		pulse_init = self.getPulse()
		temp = self.start_date + timedelta(days=-1)
		df_start_date = temp.strftime('%Y:%m:%d')
		df_end_date = self.end_date.strftime('%Y:%m:%d')
		year1, year2 = df_start_date[:4], df_end_date[:4]
		
		# Match up pulse data indices with DataFrame date indices
		pulse, pulse_time = np.array([]), []
		holidays1, holidays2 = self.createHolidayCalendar(year1), None
		if year1!=year2: holidays2 = createHolidayCalendar(year2)# If necessary, also set up year2 holidays for the second year
		
		pulse_init = self.getPulse()

		# For each Pulse datapoint, only append to self.pulse if it's corresponding date is validTradingDay
		for i in pulse_init:
			for j in i.keys():
				if j[:4]==year1:
					if self.isValidTradingDay(j[:10]):
						pulse_time.append(j)
						pulse = np.append(pulse, i[j])
				elif j[:4]==year2:
					if self.isValidTradingDay(j[:10]):
						pulse_time.append(j)
						pulse = np.append(pulse, i[j])

		return pulse, pulse_time

	def getPulse(self):
		s, e = self.start_date.strftime('%y:%m:%d'), self.end_date.strftime('%y:%m:%d')
		parameters = {'ticker': self.symbol, 'from_datetime': "20"+s+':08:30:00', 'until_datetime' : "20"+e+':08:30:00', 'agg_mode': 'D'}
		return(requests.get('http://mars.larium.ai:8002/tweets/get_pulse', params=parameters).json())

# (2) Plots - Two Different Types Available

	def makePlots(self):
		df = self.getData()
		time, volume = df.iloc[:,0].values, df.iloc[:,2].values
		close, pulse = df.iloc[:,1].values, self.createPulse()[0]
		
		"""
		def twoSubplots(time, volume, price, pulse):
			fig = make_subplots(rows=1, cols=2, subplot_titles=(
				f'Daily Price of {self.symbol}', 
				f'Daily Pulse of {self.symbol}'))
			fig.add_trace(
				go.Scatter(x=time, y=volume),
				row=1, col=1)

			fig.add_trace(
				go.Scatter(x=time, y=pulse),
				row=1, col=2)

			fig['layout']['xaxis']['title']='Time'
			fig['layout']['xaxis2']['title']='Time'
			fig['layout']['yaxis']['title']='Daily Volume'
			fig['layout']['yaxis2']['title']='Daily Pulse'

		return fig
		"""
	
		# def secondaryY(time, volume, price, pulse):
		fig = make_subplots(specs=[[{"secondary_y": True}]])

		fig.add_trace(
			go.Scatter(x=time, y=volume, name="Volume"),
			secondary_y=False,
		)

		fig.add_trace(
			go.Scatter(x=time, y=pulse, name="Pulse"),
			secondary_y=True,
		)

		# Add figure title
		fig.update_layout(
			title_text="Volume vs. Pulse"
		)
		# Set x-axis title
		fig.update_xaxes(title_text="Time")

		# Set y-axes titles
		fig.update_yaxes(title_text="Volume", secondary_y=False)
		fig.update_yaxes(title_text="Pulse Data", secondary_y=True)
		
		st.plotly_chart(fig)
		st.caption("https://iexcloud.io Data provided by IEX Cloud")
		st.write("Pearson Correlation between variables: " + str(np.corrcoef(pulse, volume)[1]))

	
	# (3) RUN
	def streamRun(self):
		if self.start_date >= self.end_date:
			st.error("Please select an end date that is after the start date.")
			return

		t = self.end_date - date.today()
		if abs(t.total_seconds()) <= 345600:
			st.error("Please select an end date that is at least four days before today.")
		diff = self.end_date - self.start_date
		if diff.total_seconds() >= 18057600:
			st.error("Please select a time frame shorter than 209 days, or 7 months.")
			return
		self.makePlots()


	
	# (4) UTILITY METHODS
	
	"""
	Next Two Methods (A) & (B) : Convert OG date to date good for pulse API/Streamlit.date_input returns a date in ISO 8601 
	format of year-month-day such as 2021-11-02, but it is a datetime object
	"""
	def isoToAPI(self, isodate):
		year = self.yearISO(isodate)
		array, result = [year, isodate[5:7], isodate[8:]], ""
		for part in array: result += part+":"
		return(result)

	def yearISO(self, isodate):
		return isodate[:4]

# (C) Valid trading day boolean: False if weekend or trading holiday
	def isValidTradingDay(self, isodate):
		holidays = self.createHolidayCalendar(isodate[:4])
		day = date.fromisoformat(isodate).isoweekday()
		status = holidays.get(isodate)
		if day==6 or day==7 or status!= None:
			return False
		else:
			return True

# (D) Create list of trading holidays in US, to filter out datapoints from pulse API
	def createHolidayCalendar(self, year):
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

		return us_holidays

tickers = [
	"AAPL",
	"MSFT",
	"GOOG",
	"AMZN",
	"TSLA",
	"FB",
	"NVDA",
	"BRK-A",
	"TSM",
	"TCEHY",
	]

visual = Visualizer(st.selectbox("Ticker", tickers), st.date_input("Start"), st.date_input("End"))
visual.streamRun()







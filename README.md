# Streamlit-FinData-Visualizer

## Overview
I saw my primary task as creating a visualization tool that could clearly display Pulse, Volume, and Price Data for any equity in a way that would show their correlation.
The main hurdle of the project was to hack the data from the API together with data from PyEX, and the display was relatively simple.

## Data
Data pulled from the Athena API needed to be cleaned for any weekend days or Holidays Days. To do this, I created the createHolidayCalendar method to create a complete list of trading holidays, as available holiday calendars were missing several trading holidays, the isValidTradingDay method to check if a day matches a trading holiday/weekend, and then broke the process of retrieving pulse data down into two: (1) Query the Athena API (2) Clean the data for non-valid trading days. 
<br />
For pulse, I chose to measure the pulse at 08:30 daily and compare it to the day's finishing trade volume. The reason for this is that ideally, pulse is meant to be an indicator of how an equity will perform in the future, so it was fitting to check a stock's pulse before the market opens in order to estimate how it would perform that day.

<br /> 
Close price and volume data was pulled from PyEX as a DataFrame using the chartDF method, and then aligned with corresponding data from the Pulse API. I chose the chartDF method and not the regular API query because it was cleaner and allowed me to confirm that I had matched up the data points correctly.

## Plots
From the Visualizations Posted, it was clear that the only feasible options for visualization was one plot with a secondary Y axis to graph both volume/price and pulse, or showing two subplots at once, which would also allow visualization of all three features. In the desired end result, a checkbox option on the Streamlit would have allowed the user to choose either to have only one graph with both pulse and volume/price, or have multiple subplots.





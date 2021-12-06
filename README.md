# Streamlit-FinData-Visualizer

## Overview
I saw my primary task as creating a visualization tool that could clearly display Pulse, Volume, and Price Data for any equity in a way that would show their correlation.
The main hurdle of the project was to hack the data from the API together with data from PyEX, and the display was relatively simple.

## Data
Data pulled from the Athena API needed to be cleaned for any weekend days or Holidays Days (thus the createHolidayCalendar and isValidTradingDay methods). 
Market data was pulled from PyEX as a DataFrame using the chartDF method, and then aligned with corresponding data from the Pulse API. I chose the chartDF method and not the regular API query because it was cleaner and allowed me to confirm that I had matched up the data points correctly.

## Plots
From the Visualizations Posted, it was clear that the only feasible options for visualization was one plot with a secondary Y axis to graph both volume/price and pulse, or showing two subplots at once, which would also allow visualization of all three features. In the desired end result, a checkbox option on the Streamlit would have allowed the user to choose either to have only one graph with both pulse and volume/price, or have multiple subplots.





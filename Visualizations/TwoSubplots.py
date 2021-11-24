import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go


df = pd.read_pickle("TeslaDFActual.pkl")

time = df.iloc[:,0].values
close = df.iloc[:,1].values
volume = df.iloc[:,2].values
pulse = df.iloc[:,3].values

fig = make_subplots(rows=1, cols=2, subplot_titles=('Daily Volume of TSLA', 'Daily Close of TSLA'))

fig.add_trace(
	go.Scatter(x=time, y=volume),
	row=1, col=1)

fig.add_trace(
	go.Scatter(x=time, y=close),
	row=1, col=2)

fig['layout']['xaxis']['title']='Time'
fig['layout']['xaxis2']['title']='Time'
fig['layout']['yaxis']['title']='Daily Volume'
fig['layout']['yaxis2']['title']='Daily Close Price'

fig.show()

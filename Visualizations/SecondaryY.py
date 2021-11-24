import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df = pd.read_pickle("TeslaDFActual.pkl")

time = df.iloc[:,0].values
close = df.iloc[:,1].values
volume = df.iloc[:,2].values

# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig.add_trace(
    go.Scatter(x=time, y=volume, name="Volume"),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=time, y=close, name="Pulse"),
    secondary_y=True,
)

# Add figure title
fig.update_layout(
    title_text="Close vs. Volume"
)

# Set x-axis title
fig.update_xaxes(title_text="Time")

# Set y-axes titles
fig.update_yaxes(title_text="Volume Data", secondary_y=False)
fig.update_yaxes(title_text="Close Data", secondary_y=True)

fig.show()
import plotly.express as px
import pandas as pd


df = pd.read_pickle("TeslaDFActual.pkl")

fig = px.line_3d(df, x="date", y="close", z="volume", labels={
	"date":"Time",
	"close":"Close Price",
	"volume":"Volume",
})

fig.update_layout(
    title_text="Time, Close Price, & Volume"
)

fig.show()
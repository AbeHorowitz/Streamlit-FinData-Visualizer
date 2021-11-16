import streamlit as st
import pyEX as p
import plotly.express as px

#IEX Information
c = p.Client(api_token='Tpk_057363474545412b9a53956f425fa12d', version='sandbox')

#Streamlit Initialization

#Get Data

df = c.chartDF(symbol='TSLA', timeframe='5y')[['close', 'volume']]
df = df.reset_index()

#Plotly Set Up
fig = px.line(df, x="date", y="close", title='Close Price of Tesla - Past 5 Years')

fig.update_layout(
    title={
        'text': "Close Price of Tesla - Past 5 Years",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})


#Streamlit Show
st.plotly_chart(fig)

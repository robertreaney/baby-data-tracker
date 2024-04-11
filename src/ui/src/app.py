import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from sheets import SheetsAPI
from visuals import grouped_feeding_info_table, diaper_info_table, grouped_feeding_histogram

DAY_CUTOFF = 10

client = SheetsAPI('.secrets/service.json')
nursing, diapers = client()
# add a "Day" label to the days encountered

st.title('Baby Data')

# ['white' for _ in range(len(cols)-1)]+['yellow']
overview_table_output = client.get_days_metrics(nursing, diapers, DAY_CUTOFF)
fill_colors = [['white' for _ in range(len(row))] for row in overview_table_output]

# color the today/yesterday column red in a cell if its less than median
for col in [-3]:
    for i, value in enumerate(overview_table_output[col]):
        if value < overview_table_output[2][i]:
            fill_colors[col][i] = 'red'
        if value >= overview_table_output[3][i]:
            fill_colors[col][i] = 'gold'

fig = go.Figure(data=[go.Table(
    header=dict(
        values=['QoI', 'Avg', 'Median', 'High Score', 'Yesterday', 'Today', 'Expected'], 
        font=dict(size=14)),
    cells=dict(values=overview_table_output,fill=dict(color=fill_colors)))])

st.plotly_chart(fig, use_container_width=True)

# grouped feeding info
st.plotly_chart(grouped_feeding_info_table(nursing), use_container_width=True)

st.plotly_chart(grouped_feeding_histogram(nursing, 72), use_container_width=True)

# daily diaper info
st.plotly_chart(diaper_info_table(diapers), use_container_width=True)

# lets make a time history of some of our stats for a line plot
df1 = nursing.groupby('Adjusted_Date').agg({
    'Minutes': lambda x: x.sum() / 60,
    'Dad': 'sum',
    'Mom': 'sum',
    'Margot': 'sum'
})
df2 = diapers.groupby('Adjusted_Date').agg({'Type': 'count'})

df = pd.merge(df1, df2, on='Adjusted_Date', how='outer')
df = df.rename(columns={'Minutes': 'Feeding', 'Type': 'Diapers'})

# only care about the last week
df = df[-7:-1]

fig = px.line(df.reset_index(), x='Adjusted_Date', y=['Feeding', 'Diapers'], title='Food & Poop', color_discrete_sequence=['blue', 'red'])

# Customize the x-axis to show dates in '%m/%d' format and rotate the labels for better readability
fig.update_xaxes(tickformat='%m/%d', tickangle=45)

st.plotly_chart(fig, use_container_width=True)


sleep_fig = px.line(df.reset_index(), x='Adjusted_Date', y=['Mom','Dad', 'Margot'], title='Sleep')

sleep_fig.update_xaxes(tickformat='%m/%d', tickangle=45)

st.plotly_chart(sleep_fig, use_container_width=True)
from datetime import datetime, timedelta
from pytz import timezone
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from views import grouped_feeding_info, daily_diaper_info

TZ = timezone('US/Eastern')
NOW = datetime.now(tz=TZ)

def diaper_info_table(df):
    df = daily_diaper_info(df)

    values = [df.columns.tolist()]
    values += df.values.tolist()

    fig = go.Figure(data=go.Table(
        header=dict(
            values=['QoI', '24h', '24h-48h'],
            font={'size': 14}
            ),
        cells={'values': values}
        )
    )

    fig.update_layout({'title_text': 'Prev 48h Diapers'})

    return fig


    
def grouped_feeding_info_table(df):
    # TODO most of this should go into the view creation
    df = grouped_feeding_info(df)

    df['End'] = df.End.dt.tz_localize(TZ)
    df['Start'] = df.Start.dt.tz_localize(TZ)

    data = {
        'Average Duration': [],
        'Median Duration': [],
        'Average Gap': [],
        'Median Gap': []
    }

    for delta in [24, 48, 24*7]:
        time = (NOW - timedelta(hours=delta))
        avg_duration = df[df.Start >= time].Minutes.mean()
        med_duration = df[df.Start >= time].Minutes.median()
        avg_gap = df[df.Start >= time].time_between_feeding.mean()
        med_gap = df[df.Start >= time].time_between_feeding.median()


        data['Average Duration'].append(round(avg_duration,2))
        data['Median Duration'].append(round(med_duration,2))
        data['Average Gap'].append(f'{avg_gap.components.hours}:{avg_gap.components.minutes:02d}')
        data['Median Gap'].append(f'{med_gap.components.hours}:{med_gap.components.minutes:02d}')

    df = pd.DataFrame(data)

    values = [df.columns.tolist()]
    values += df.values.tolist()

    fig = go.Figure(data=go.Table(
        header=dict(
            values=['QoI', '24h', '48h', '1w'],
            font={'size': 14}
            ),
        cells={'values': values}
        )
    )

    fig.update_layout({'title_text': 'Grouped Nursing Data'})

    return fig


def grouped_feeding_histogram(df, hours=72):
    # TODO most of this should go into the view creation
    df = grouped_feeding_info(df)

    df['End'] = df.End.dt.tz_localize(TZ)
    df['Start'] = df.Start.dt.tz_localize(TZ)

    time = (NOW - timedelta(hours=hours))

    data = df[df.Start >= time]
    hist = px.histogram(data, x='Minutes', nbins=10)

    # Adding title and labels
    hist.update_layout(
        title_text=f'{hours}h Feeding Histogram', # title of plot
        xaxis_title_text='Value', # xaxis label
        yaxis_title_text='Count', # yaxis label
        bargap=0.2, # gap between bars of adjacent location coordinates
    )

    return hist
import pandas as pd
from datetime import datetime, timedelta
from pytz import timezone

# 1) avg feed time
    # graph of last 3 days?
    # avg of last day/2days?
# 2) avg time between feedings
# 3) last 24 hours info
    # number diapers

TZ = timezone('US/Eastern')
NOW = datetime.now(tz=TZ)

def daily_diaper_info(df):
    df['Time'] = df.Time.dt.tz_localize(TZ)

    data = {
        'Wet': [],
        'Poop': [],
        'Total': []
    }

    end = NOW
    start = (NOW - timedelta(hours=24))

    for day in range(2):
        subset = df[(df.Time <= end) & (df.Time >= start)]

        data['Total'].append(len(subset))
        data['Wet'].append(len(subset[(subset.Type == 'Wet') | (subset.Type == 'Both')]))
        data['Poop'].append(len(subset[(subset.Type == 'Poop') | (subset.Type == 'Both')]))

        end = start
        start -= timedelta(hours=24)

    result = pd.DataFrame(data)

    return result


def grouped_feeding_info(df):
    GAP = 30    # minutes between feedings to qualify for collapse
    result = []
    current_minutes = 0
    current_start = None
    current_end = None

    for _, row in df.iterrows():
        # if fresh group or the next row is close enough to the current end
        if current_end is None or row['Start'] <= current_end + pd.Timedelta(minutes=GAP):
            if current_start is None:
                current_start = row['Start']
            
            current_end = row['End']
            current_minutes += row['Minutes']

        # save the current group and start a new group
        else:
            result.append({
                'Start': current_start,
                'End': current_end,
                'Minutes': current_minutes
            })

            current_minutes = row['Minutes']
            current_start = row['Start']
            current_end = row['End']

    # save the final iteration values
    if current_end is not None:
        result.append({
            'Start': current_start,
            'End': current_end,
            'Minutes': current_minutes
        })

    result = pd.DataFrame(result)

    result['prev_end'] = result['End'].shift(1)
    result['time_between_feeding'] = result['Start'] - result['prev_end']

    return result

if __name__ == '__main__':
    from sheets import SheetsAPI

    client = SheetsAPI('.secrets/service.json')
    nursing, diapers = client()

    df = grouped_feeding_info(nursing)

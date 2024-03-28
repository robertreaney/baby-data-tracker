import os.path
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import pandas as pd
import numpy as np

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1-dVuM5U5sxgZysPauet_LkSaE78s4PpUE-KNUdGVyv0"
NURSING_RANGE = "Nursing!A:J"
DIAPERS_RANGE = "Diapers!A:C"
CREDS = '.secrets/service.json'

class SheetsAPI:
  def __init__(self, path=CREDS):
    creds = None

    if os.path.exists(path):
      creds = Credentials.from_service_account_file(path)
    else:
      raise ValueError('no creds found')
    
    try:
      self.service = build("sheets", "v4", credentials=creds)
    except Exception as e:
      raise ValueError(f'Error connecting to sheets service: {e}')

  def __call__(self):
    nursing, diapers = self.fetch()
    return self.process_nursing(nursing), self.process_diapers(diapers)

  def fetch(self):

    output = []
    for SAMPLE_RANGE_NAME in [NURSING_RANGE, DIAPERS_RANGE]:
      # Call the Sheets API
      sheet = self.service.spreadsheets()
      result = (
          sheet.values()
          .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
          .execute()
      )
      values = result.get("values", [])

      df = pd.DataFrame(values[1:], columns=values[0])

      output.append(df)

    return output
  
  def process_diapers(self, df):
    df = df.replace('', np.nan).astype({
      'Time': 'datetime64[ns]',
      'Type': str,
      'Notes': str
    })

    df = df.sort_values(by='Time')
    return df

  def process_nursing(self, df):

    df = df[df.Minutes!='0']

    df = df.replace('', np.nan).astype({
      'Start': 'datetime64[s]',
      'End': 'datetime64[s]',
      'Minutes': int,
      'Boob': str,
      'Dad': float,
      'Mom': float,
      'Margot': float,
      'Supplement': str,
      'Quality': str,
      'Notes': str
    })

    df = df.sort_values(by='Start')
    return df
  
  def chunk_days(self, df, date_col, cutoff_hour=None):
    if cutoff_hour:
      df['Adjusted_Start'] = df[date_col] - pd.Timedelta(hours=cutoff_hour)
    else:
      df['Adjusted_Start'] = df[date_col]

    # create date column
    df['Adjusted_Date'] = df['Adjusted_Start'].dt.date

    return df
  
  def get_days_metrics(self, nursing, diapers, cutoff_hour=None):

    nursing = self.chunk_days(nursing, date_col='Start', cutoff_hour=cutoff_hour)
    diapers = self.chunk_days(diapers, date_col='Time', cutoff_hour=cutoff_hour)

    qois = ['Minutes', 'Dad', 'Mom', 'Margot']
    values = [[group[x].sum() for name, group in nursing.groupby('Adjusted_Date')] for x in qois] 

    # append diapers info
    qois += ['# Diapers']
    values += [[len(group) for name, group in diapers.groupby('Adjusted_Date')]]

    # pop today so it isn't used in mean calculations and record yesterday
    today = [round(x.pop(),2) for x in values]
    yesterday = [round(x[-1], 2) for x in values]

    # need to remove 0s and round to nearest hundreth
    cleaned_values = [[item for item in sublist if item != 0] for sublist in values]
    
    # needs to return values=[[qois], [avgs], [medians], [today's values]]
    overview_table_output = [
      qois,
      [round(np.mean(l),2) for l in cleaned_values], # avgs
      [round(np.median(l),2) for l in cleaned_values], # medians
      [round(np.max(l), 2) for l in cleaned_values], # maximum
      yesterday,
      today # today
    ]

    return overview_table_output

    



if __name__ == "__main__":
  sheets = SheetsAPI()

  values = sheets()

  days = sheets.get_days_metrics(values, 8)

  print(values)
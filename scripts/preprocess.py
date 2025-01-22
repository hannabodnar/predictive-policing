import pandas as pd
import sqlite3
from datetime import datetime

# Load data
data = pd.read_csv('Crime_Data_from_2020_to_Present.csv', sep=',', header=0)

# Remove unnecessary columns
data = data.drop(columns=['Part 1-2', 'Mocodes', 'Status', 'Crm Cd 1', 'Crm Cd 2', 'Crm Cd 3', 'Crm Cd 4', 'LOCATION', 'Cross Street'], axis=1)

# Rename Column
data = data.rename(columns={'Crm Cd Desc': 'Crime Desc', 'Crm Cd': 'Crime Code', 'Premis Cd': 'Premis Code', 'AREA': 'Area Code'})

# Convert Date rptd and Date Occ to datetime format
date_cols = ['Date Rptd', 'DATE OCC']
data[date_cols] = data[date_cols].apply(pd.to_datetime, format='%m/%d/%Y %I:%M:%S %p')

# Remove timestamp from dates
data['Date Rptd'] = data['Date Rptd'].apply(lambda x: x.date())
data['DATE OCC'] = data['DATE OCC'].apply(lambda x: x.date())

# Multiple counts of values = 1, 5 are found in Time OCC column with no interpretation.
# Due to size of dataset, rows with those values will be removed.

#print(data['TIME OCC'].value_counts()[5])
data = data.drop(data[data['TIME OCC'] == 5].index)

#print(data['TIME OCC'].value_counts()[1])
data = data.drop(data[data['TIME OCC'] == 1].index)

# Remove all other non-time values
time_df = data.loc[data['TIME OCC'] < 100]
values = time_df['TIME OCC'].value_counts()
val_list = list(set(time_df['TIME OCC']))
rows = data[data['TIME OCC'].isin(val_list)].index
data = data.drop(rows)

# Change time format in TIME OCC to 24 hr
data['TIME OCC'] = data['TIME OCC'].apply(lambda x: datetime.strptime(str(x).zfill(4), '%H%M').time())

# Find all NULL values
null_df = data[data.isnull().any(axis=1)]
data['Vict Sex'] = data['Vict Sex'].fillna('X')  # Replace NULL with X
data['Vict Descent'] = data['Vict Descent'].fillna('X')  # Replace NULL with X
data['Premis Desc'] = data['Premis Desc'].fillna('UNKNOWN')
data['Premis Code'] = data['Premis Code'].fillna(000.)
data['Weapon Desc'] = data['Weapon Desc'].fillna('UNKNOWN WEAPON/OTHER WEAPON')
data['Weapon Used Cd'] = data['Weapon Used Cd'].fillna(500.)
print(data[data.isnull().any(axis=1)])


# Change negative values to 0 for Victim Age
#print(data[data['Vict Age'] < 0])
data.loc[data['Vict Age'] < 0, 'Vict Age'] = 0
#print(data[data['Vict Age'] < 0])

# Replace H with X in Vict Sex column to signify unknown
data['Vict Sex'] = data['Vict Sex'].replace('H', 'X')

# Change value for Victim Sex and Descent to Unknown for specific input
rpt_idx = data.index[data['Vict Sex'] == '-']
data.loc[rpt_idx[0], 'Vict Sex'] = 'X'
data.loc[rpt_idx[0], 'Vict Descent'] = 'X'

desc_idx = data.index[data['Vict Descent'] == '-']
data.loc[desc_idx[0], 'Vict Descent'] = 'X'

crime_counts = data['Crime Desc'].value_counts()
crime_drops = crime_counts[crime_counts < 11].index
data = data[~data['Crime Desc'].isin(crime_drops)]

# SQL Database to view changes
db_path = 'clean_data.db'
conn = sqlite3.connect(db_path)
data.to_sql('clean_data', conn, if_exists='replace', index=False)
conn.close()

# Create CSV file
data.to_csv('cleaned_data.csv', index=False)


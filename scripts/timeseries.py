import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import seaborn as sns

# Load Data
data = pd.read_csv('aggragated_data.csv')

# Change variables to datetime format
date_cols = ['Date Rptd', 'DATE OCC']
data[date_cols] = data[date_cols].apply(pd.to_datetime)
data['TIME OCC'] = pd.to_datetime(data['TIME OCC'], format='%H:%M:%S')

data = data.sort_values(by=['DATE OCC'])
week_intervals = pd.date_range(start=data['DATE OCC'].dt.date.min(), end=data['DATE OCC'].dt.date.max(), freq='W')
victim_demographics_time_series = data.groupby([pd.cut(data['DATE OCC'].dt.date, bins=week_intervals), 'Vict Descent']).size().unstack(fill_value=0)
victim_demographics_time_series.index = victim_demographics_time_series.index.map(lambda x: x.left)
print(victim_demographics_time_series)
#victim_demographics_time_series.index.name = pd.DataFrame(victim_demographics_time_series.index)
print(victim_demographics_time_series)

crime_data_grouped = data.groupby(['AREA NAME', pd.cut(data['DATE OCC'].dt.floor('D'), week_intervals)]).size().unstack()
crime_data_grouped = pd.DataFrame(crime_data_grouped)
crime_data_grouped = crime_data_grouped.T
#crime_data_grouped.index = pd.to_datetime(crime_data_grouped.index)

#crime_data_grouped['DATE OCC'] = pd.to_datetime(crime_data_grouped['DATE OCC'])



weekly_crime_count = data.groupby(pd.cut(data['DATE OCC'].dt.date, bins=week_intervals)).apply(lambda x: x['Crime Type'].value_counts().idxmax())

data.set_index('DATE OCC', inplace=True)
data_resample = data.resample('W').size()


custom_palette = sns.color_palette("husl", n_colors=len(victim_demographics_time_series.columns))

# Plot the victim demographics time series using Seaborn
plt.figure(figsize=(12, 8))
sns.set_style("whitegrid")  # Optional: set the style
sns.lineplot(data=victim_demographics_time_series, palette=custom_palette, dashes=False)
plt.title('Victim Descent Time Series')
plt.xlabel('Time')
plt.ylabel('Number of Crime Incidents')
plt.legend(title='Victim Descent', loc='center left', bbox_to_anchor=(1, 0.5))

# Show the plot
plt.tight_layout()  # Ensure labels fit within the figure
plt.savefig('Victim Descent Time Series.png')
plt.show()


plt.figure(figsize=(10, 6))
data_resample.plot(color='blue', linestyle='-')
plt.title('Total Number of Crime Incidents Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Crime Incidents')
plt.grid(True)
plt.savefig('crime_time.png')
plt.show()
#print(data['DATE OCC'])

result = seasonal_decompose(data_resample, model='additive')

plt.figure(figsize=(10, 6))
plt.subplot(411)
plt.plot(result.observed, label='Observed')
plt.legend()

plt.subplot(412)
plt.plot(result.trend, label='Trend')
plt.legend()

plt.subplot(413)
plt.plot(result.seasonal, label='Seasonal')
plt.legend()

plt.subplot(414)
plt.plot(result.resid, label='Residual')
plt.legend()

plt.tight_layout()
#plt.savefig('additive_time.png')
plt.show()



train_size = 0.7
split_idx = int(train_size * len(data_resample))
train_data, test_data = data_resample[:split_idx], data_resample[split_idx:]

#train_data = pd.to_datetime(train_data.index)
#test_data = pd.to_datetime(test_data.index)

# Define the forecasting period based on the entire dataset


train_data_series = pd.Series(train_data)
test_data_series = pd.Series(test_data)
test_date_series = pd.Series(test_data.index)
min_date = test_date_series.min()
max_date = test_date_series.max()
print(test_date_series)
model = ExponentialSmoothing(train_data_series, trend='additive', seasonal='additive', initialization_method='estimated', seasonal_periods=7)
result = model.fit()

# Forecast future values
forecast = result.predict(start=min_date, end=max_date)

# Evaluate the forecast
mse = ((forecast - test_data_series) ** 2).mean()
print("Mean Squared Error:", mse)



#sarima_model = sm.tsa.SARIMAX(train_data, order=order, seasonal_order=season_order)
#sarima_result = sarima_model.fit()

# Make forecasts
#forecast = sarima_result.predict(start=min_date, end=max_date, dynamic=True)

# Evaluate model performance
# For example, calculate Mean Absolute Error (MAE)
#mae = mean_absolute_error(test_data, forecast)


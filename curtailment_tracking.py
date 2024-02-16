from database_collector import fpn_data_collector
import pandas as pd
import matplotlib.pyplot as plt

# Function to get start and end dates based on user selection
def get_start_end_dates(interval):
    if interval == 'day':
        start_date = input("Enter the date (YYYY-MM-DD) for the day: ")
        end_date = pd.to_datetime(start_date) + pd.DateOffset(days=1)
    elif interval == 'week':
        start_date = input("Enter the date (YYYY-MM-DD) for the week (Monday): ")
        start_date = pd.to_datetime(start_date) - pd.DateOffset(days=pd.to_datetime(start_date).dayofweek)
        end_date = start_date + pd.DateOffset(weeks=1)
    elif interval == 'month':
        month = input("Enter the month (YYYY-MM) for the month: ")
        start_date = pd.to_datetime(month + '-01')
        end_date = start_date + pd.DateOffset(months=1)
    elif interval == 'year':
        start_date = pd.to_datetime('2023-01-01')
        end_date = start_date + pd.DateOffset(years=1)
    else:
        raise ValueError("Invalid interval selected. Please choose day, week, month, or year.")
    
    return start_date, end_date

# User input for the desired interval
selected_interval = input("Select the interval (day/week/month/year): ").lower()

# Get start and end dates based on user selection
start_date, end_date = get_start_end_dates(selected_interval)

# Additional inputs (BMU selection, etc.) can be added here if needed
bmu = 'E_MOYEW-1'

# Collect the dataset using the function from database_collector.py
fpn_df = fpn_data_collector(start_date.strftime('%Y-%m-%d %H:%M'), end_date.strftime('%Y-%m-%d %H:%M'), bmu)

# Assuming 'ts' column is not in datetime format, convert it
fpn_df['ts'] = pd.to_datetime(fpn_df['ts'])

# Set the 'ts' column as the index
fpn_df.set_index('ts', inplace=True)

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(fpn_df.index, fpn_df['vp'], label='Final Physical Notification')
plt.title('Time vs MW Plot for BMU_ID')
plt.xlabel('Time')
plt.ylabel('MW Values')
plt.legend()
plt.show()


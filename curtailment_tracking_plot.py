from database_collector import fpn_data_collector, boalf3_data_collector, abv_data_collector
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
from datetime import datetime, timedelta
import numpy as np

#----------------------------------------------------------------------------------------------------------------#
# FUNCTIONS
#----------------------------------------------------------------------------------------------------------------#

# Define the function to merge sd and sp to timestamp
def merge_sd_sp_to_timestamp(sd, sp):
    date_obj = datetime.strptime(sd, '%Y-%m-%d')
    time_delta = timedelta(minutes=(int(sp) - 1) * 30)
    timestamp = date_obj + time_delta
    timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M')
    return timestamp_str

#----------------------------------------------------------------------------------------------------------------#

# Function to convert timestamp to matplotlib-compatible format
def convert_to_mpl_datetime(ts_str):
    return pd.to_datetime(ts_str).to_numpy()

#----------------------------------------------------------------------------------------------------------------#

# Function to create plot for BMU comparison
def BMU_plot_comparator(fpn_df, boalf_df, abv_df, bmu):
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.subplots_adjust(left=0.2)

    lines = []
    labels = []

    # Plot FPN data
    if not fpn_df.empty:
        line1, = ax.plot(convert_to_mpl_datetime(fpn_df['ts']), fpn_df['vp'], marker='o', label=f'{bmu} - Final Physical Notification')
        lines.append(line1)
        labels.append(f'{bmu} - Final Physical Notification')

    # Plot BOALF data
    if not boalf_df.empty:
        boalf_df['ts'] = pd.to_datetime(boalf_df['ts'])  # Convert 'ts' to datetime
        boalf_df['time_diff'] = boalf_df['ts'].diff().dt.total_seconds() / 60.0  # Calculate time differences in minutes
        split_indices = boalf_df[boalf_df['time_diff'] > 30].index.tolist()
        split_indices.insert(0, 0)
        split_indices.append(len(boalf_df))

        for i in range(len(split_indices) - 1):
            sub_boalf_df = boalf_df.iloc[split_indices[i]:split_indices[i + 1]]
            line, = ax.plot(sub_boalf_df['ts'], sub_boalf_df['va'], marker='o', label=f'{bmu} - BOALF {i + 1}', color='orange')
            lines.append(line)
            labels.append(f'{bmu} - BOALF {i + 1}')

    # Plot ABV data
    if not abv_df.empty:
        abv_df['sd'] = abv_df['sd'].astype(str)  # Convert 'sd' to string
        abv_df['ts'] = abv_df.apply(lambda row: merge_sd_sp_to_timestamp(row['sd'], row['sp']), axis=1)
        line3, = ax.plot(convert_to_mpl_datetime(abv_df['ts']), abv_df['vol'], marker='o', label=f'{bmu} - ABV', color='blue')
        lines.append(line3)
        labels.append(f'{bmu} - ABV')

    ax.legend(lines, labels, loc='upper left')  # Adjust legend position
    ax.set_title(f'Time vs MW Plot for {bmu}')
    ax.set_xlabel('Time')
    ax.set_ylabel('MW Values')
    ax.tick_params(axis='x', rotation=90)

    # Add a toggle button
    ax_toggle = plt.axes([0.02, 0.5, 0.1, 0.06])  # Adjust position of toggle box within the figure
    check = CheckButtons(ax_toggle, ['FPN', 'BOALF', 'ABV'], [True, True, True])

    def toggle_func(label):
        for line in lines:
            if label in line.get_label():
                line.set_visible(not line.get_visible())
        plt.draw()

    check.on_clicked(toggle_func)

    plt.show()

#----------------------------------------------------------------------------------------------------------------#

def calculate_percentage_difference(fpn_df, boalf_df, abv_df):
    # Extract BOALF intervals and create a list of intervals to exclude
    boalf_intervals = boalf_df['ts']
    exclude_intervals = []

    for boalf_time in boalf_intervals:
        boalf_start = boalf_time - timedelta(minutes=15)
        boalf_end = boalf_time + timedelta(minutes=15)
        exclude_intervals.append((boalf_start, boalf_end))

    # Exclude intervals overlapping with BOALF times from FPN data
    fpn_df['interval_start'] = pd.to_datetime(fpn_df['ts']) - timedelta(minutes=15)
    fpn_df['interval_end'] = pd.to_datetime(fpn_df['ts']) + timedelta(minutes=15)
    
    # Handle the case where there are two values for a specific FPN 30-minute interval
    fpn_df['vp'] = fpn_df.groupby(['sd', 'sp'])['vp'].transform('mean')
    fpn_df = fpn_df.drop_duplicates(subset=['sd', 'sp'], keep='first')
    
    fpn_df = fpn_df[~fpn_df.apply(lambda row: any(((row['interval_start'] <= end) and (row['interval_end'] >= start))
                                                  for start, end in exclude_intervals), axis=1)]

    # Group by 'sd' and 'sp' in FPN data and calculate the sum for 'vp'
    fpn_sum_df = fpn_df.groupby(['sd', 'sp'], as_index=False)['vp'].sum()

    # Merge datasets on 'sd' and 'sp'
    merged_df = pd.merge(fpn_sum_df, abv_df, on=['sd', 'sp'], how='inner', suffixes=('_fpn', '_abv'))

    # Calculate total differences between 'vol' and 'vp'
    total_vol = merged_df['vol'].sum()
    total_vp = merged_df['vp'].sum()

    # Calculate percentage difference, handle division by zero
    percentage_difference = ((total_vol - total_vp) / total_vp)
    percentage_difference = np.nan_to_num(percentage_difference) * 100

    print(f'\nTotal ABV (vol): {total_vol} MW')
    print(f'Total FPN (vp): {total_vp} MW')
    print(f'Percentage Difference: {round(percentage_difference, 2)}%')

#----------------------------------------------------------------------------------------------------------------#



#----------------------------------------------------------------------------------------------------------------#

def calculate_total_percentage_difference(fpn_df, abv_df):
    # Calculate total differences between 'vol' and 'vp'
    total_vol = abv_df['vol'].sum()
    total_vp = fpn_df['vp'].sum()

    # Calculate percentage difference, handle division by zero
    percentage_difference = ((total_vol - total_vp) / total_vp)
    percentage_difference = np.nan_to_num(percentage_difference) * 100

    print(f'\nTotal Vol: {total_vol} MWh')
    print(f'Total VP: {total_vp} MWh')
    print(f'Percentage Difference: {round(percentage_difference, 2)}%')


#----------------------------------------------------------------------------------------------------------------#
# MAIN SECTION OF SKIPRATE SCRIPT 
#----------------------------------------------------------------------------------------------------------------#

# Define the variables for interval selection and BMU ID
start_date = '2023-01-01'  # Example: 'YYYY-MM-DD'
end_date = '2023-02-01'  # Must be the day above the final day you desire
bmu = 'T_FARR-1'  
# Windfarms:                    10 days, 1 month (-ve: FPN larger than output)
#   'E_MOYEW-1' - FPN above, -21.00%, -28.53%
#   'T_FARR-1' - FPN over estimates, -67.72%, -24.6%
#   'T_GLNKW-1' - FPN very good, 3.05%, 3.3%
#   'T_DUNGW-1' - FPN above, evidence of turbine shut down, -13.59%, -10.62%
#   'T_STLGW-1' - FPN potential gaming, -6.74%, -5.88%
#   'E_HLGLW-1' - FPN way above, doesnt look like gaming, -31.71%, -35.09%
#   'T_DNLWW-1' - FPN very good, 4.05%, 0.94% 

# Collect the dataset using the functions for the BMU
fpn_df = fpn_data_collector(start_date, end_date, bmu)
boalf_df = boalf3_data_collector(start_date, end_date, bmu)
abv_df = abv_data_collector(start_date, end_date, bmu)
abv_df['vol'] = abv_df['vol'] * 2  # Counteract the MWh values of the real generation

# Create a new dataframe with percentage differences
calculate_percentage_difference(fpn_df, boalf_df, abv_df)

calculate_total_percentage_difference(fpn_df, abv_df)

# Plot FPN, actual output, curtailment
#BMU_plot_comparator(fpn_df, boalf_df, abv_df, bmu)


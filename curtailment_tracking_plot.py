from database_collector import fpn_data_collector, boalf3_data_collector, abv_data_collector
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
from datetime import datetime, timedelta

# Define the function to merge sd and sp to timestamp
def merge_sd_sp_to_timestamp(sd, sp):
    date_obj = datetime.strptime(sd, '%Y-%m-%d')
    time_delta = timedelta(minutes=(int(sp) - 1) * 30)
    timestamp = date_obj + time_delta
    timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M')
    return timestamp_str

# Define the variables for interval selection and BMU ID
start_date = '2023-01-02'  # Example: 'YYYY-MM-DD'
end_date = '2023-01-10'  # Must be the day above the final day you desire
bmu = 'T_DNLWW-1'  
# Windfarms: 
#   'E_MOYEW-1' - FPN seems to be way above generation
#   'T_FARR-1' - FPN seems to correlate with generation
#   'T_GLNKW-1' - FPN seems to be way above generation
#   'T_DUNGW-1' - FPN seems to be way above generation
#   'T_STLGW-1' - FPN seems to be way above generation
#   'E_HLGLW-1' - FPN seems to correlate with generation
#   'T_DNLWW-1' - FPN seems to correlate with generation

# Function to convert timestamp to matplotlib-compatible format
def convert_to_mpl_datetime(ts_str):
    return pd.to_datetime(ts_str).to_numpy()

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
        line2, = ax.plot(boalf_df['ts'], boalf_df['va'], marker='o', label=f'{bmu} - BOALF', color='orange')
        lines.append(line2)
        labels.append(f'{bmu} - BOALF')

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

# Collect the dataset using the functions for the BMU
fpn_df = fpn_data_collector(start_date, end_date, bmu)
boalf_df = boalf3_data_collector(start_date, end_date, bmu)
abv_df = abv_data_collector(start_date, end_date, bmu)

# Create plot for BMU comparison
BMU_plot_comparator(fpn_df, boalf_df, abv_df, bmu)

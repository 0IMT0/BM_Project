from database_collector import fpn_data_collector, boalf3_data_collector, abv_data_collector
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np
from matplotlib.widgets import CheckButtons
from scipy.stats import linregress

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
    plt.subplots_adjust(left=0.1, bottom=0.2, right=0.8)

    lines = []
    labels = []

    # Check if there are any BOALF values
    has_boalf_values = not boalf_df.empty

    # Plot ABV data
    if not abv_df.empty:
        abv_df['sd'] = abv_df['sd'].astype(str)  # Convert 'sd' to string
        abv_df['ts'] = abv_df.apply(lambda row: merge_sd_sp_to_timestamp(row['sd'], row['sp']), axis=1)
        line3, = ax.plot(convert_to_mpl_datetime(abv_df['ts']), abv_df['vol'], marker='.', label='Real', color='dodgerblue', zorder=1)
        lines.append(line3)
        labels.append('Real')
        # Shade the area under the ABV plot
        ax.fill_between(convert_to_mpl_datetime(abv_df['ts']), abv_df['vol'], color='dodgerblue', alpha=1)

    # Plot red background for BOALF intervals
    if has_boalf_values:
        boalf_intervals = boalf_df['ts']
        for boalf_time in boalf_intervals:
            boalf_start = boalf_time - timedelta(minutes=30)
            boalf_end = boalf_time + timedelta(minutes=30)
            min_boalf_value = boalf_df[(boalf_df['ts'] >= boalf_start) & (boalf_df['ts'] <= boalf_end)]['va'].min()
            ax.fill_between(convert_to_mpl_datetime(fpn_df['ts']), min_boalf_value, fpn_df['vp'], where=((convert_to_mpl_datetime(fpn_df['ts']) >= boalf_start) & (convert_to_mpl_datetime(fpn_df['ts']) <= boalf_end)), color='indianred', alpha=1, zorder=2)
        
        # Add the 'Curtailment' label for the red area
        line_curtailment, = ax.plot([], [], color='indianred', label='Curtailment')
        lines.append(line_curtailment)

    # Plot FPN data
    if not fpn_df.empty:
        line1, = ax.plot(convert_to_mpl_datetime(fpn_df['ts']), fpn_df['vp'], marker='.', label='Forecast', color='orange', zorder=3)
        lines.append(line1)
        labels.append('Forecast')

    ax.set_title(f'Generation vs Time Plot for {bmu}', fontsize=28)
    ax.set_xlabel('Date/Time (MM-DD hh)', fontsize=24) 
    ax.set_ylabel('Generation (MW)', fontsize=24)  
    ax.tick_params(axis='x', rotation=45, labelsize=16) 
    ax.tick_params(axis='y', labelsize=16)
    ax.legend(loc='upper left', fontsize=16, bbox_to_anchor=(1.01, 0.5), borderaxespad=0)
    #ax.set_ylim([0, 65])


    # Add a toggle button
#    ax_toggle = plt.axes([0.02, 0.5, 0.1, 0.06])  # Adjust position of toggle box within the figure
#    check = CheckButtons(ax_toggle, ['FPN', 'BOALF', 'ABV'], [True, True, True])

#    def toggle_func(label):
#        for line in lines:
#            if label in line.get_label():
#                line.set_visible(not line.get_visible())
#        plt.draw()

#    check.on_clicked(toggle_func)

    plt.show()

#----------------------------------------------------------------------------------------------------------------#

def calculate_percentage_difference(fpn_df, boalf_df, abv_df, bmu, start_date, save_merged_df=False):
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

    # Calculate curtailment instruction value
    curtailment_instruction = boalf_df.shape[0]  # Number of rows in boalf_df

    print(f'\nTotal ABV (vol): {total_vol} MW')
    print(f'Total FPN (vp): {total_vp} MW')
    print(f'Percentage Difference: {round(percentage_difference, 2)}%')
    print(f'Curtailment Instructions: {curtailment_instruction}')

    if save_merged_df:
        file_name = f"percentage_data_{bmu}_{start_date}.xlsx"
        merged_df.to_excel(file_name, index=False)
        print(f'\nMerged dataframe saved as {file_name}')

    return merged_df

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
    print(f'Percentage Difference (with curtailment): {round(percentage_difference, 2)}%')

#----------------------------------------------------------------------------------------------------------------#

def generate_scatter_plot(merged_df, bmu):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Scatter plot darkorange
    ax.scatter(merged_df['vp'], merged_df['vol'], color='dodgerblue', alpha=0.5)
    
    # Calculate correlation coefficient
    correlation_coefficient = np.corrcoef(merged_df['vp'], merged_df['vol'])[0, 1]
    print(f'Correlation Coefficient: {correlation_coefficient}')

    # Perform linear regression
    slope, intercept, _, _, _ = linregress(merged_df['vp'], merged_df['vol'])
    
    # Plot line of best fit
    #ax.plot(merged_df['vp'], slope * merged_df['vp'] + intercept, color='black', label=f'Line of Best Fit (Correlation Coefficient: {correlation_coefficient:.2f})')
    
    ax.set_title(f'Real vs Forecast Generation Scatter Plot', fontsize=28)
    ax.set_xlabel('Forecast Generation (MW)', fontsize=24)
    ax.set_ylabel('Real Generation (MW)', fontsize=24)
    ax.tick_params(axis='x', rotation=45, labelsize=16) 
    ax.tick_params(axis='y', labelsize=16)
    ax.grid(True)
    ax.legend(fontsize=16)
    
    plt.show()


#----------------------------------------------------------------------------------------------------------------#
# MAIN SECTION OF SKIPRATE SCRIPT 
#----------------------------------------------------------------------------------------------------------------#

# Define the variables for interval selection and BMU ID
start_date = '2023-01-01'  # Example: 'YYYY-MM-DD'
end_date = '2023-03-10'  # Must be the day above the final day you desire
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
merged_df = calculate_percentage_difference(fpn_df, boalf_df, abv_df, bmu, start_date, save_merged_df=False)
#generate_scatter_plot(merged_df, bmu)

calculate_total_percentage_difference(fpn_df, abv_df)

# Plot FPN, actual output, curtailment
BMU_plot_comparator(fpn_df, boalf_df, abv_df, bmu)

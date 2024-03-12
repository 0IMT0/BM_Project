import pandas as pd
import numpy as np
from database_collector import fpn_data_collector, boalf3_data_collector, abv_data_collector, bmuid_data_collector
from datetime import datetime, timedelta

#----------------------------------------------------------------------------------------------------------------#
# FUNCTIONS
#----------------------------------------------------------------------------------------------------------------#

def percentage_difference(fpn_df, boalf_df, abv_df):
    try:
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

        return total_vol, total_vp, percentage_difference

    except Exception as e:
        print(f'Error in percentage_difference function: {e}')
        return 0, 0, 0  # Return default values in case of an error

#----------------------------------------------------------------------------------------------------------------#

def calculate_and_save_percentage_difference(bmu_df, start_date, end_date):
    # Create an empty DataFrame to store results
    results_df = pd.DataFrame(columns=['BMU_ID', 'Total_VOL', 'Total_VP', 'Percentage_Difference'])

    for index, row in bmu_df.iterrows():
        bmu_id = row['id']  # Change 'id' to the actual column name in your DataFrame

        # Collect the dataset using the functions for the BMU
        fpn_df = fpn_data_collector(start_date, end_date, bmu_id)
        boalf_df = boalf3_data_collector(start_date, end_date, bmu_id)
        abv_df = abv_data_collector(start_date, end_date, bmu_id)

        # Check if any of the data frames is empty, skip BMU if true
        if fpn_df.empty or boalf_df.empty or abv_df.empty:
            print(f'Skipping BMU {bmu_id} due to missing data.')
            continue

        # Calculate percentage difference
        total_vol, total_vp, percentage_diff = percentage_difference(fpn_df, boalf_df, abv_df)

        # Append the results to the DataFrame
        results_df = pd.concat([results_df, pd.DataFrame({'BMU_ID': [bmu_id],
                                                          'Total_VOL': [total_vol],
                                                          'Total_VP': [total_vp],
                                                          'Percentage_Difference': [percentage_diff]})])

    # Sort the results by Percentage Difference
    results_df = results_df.sort_values(by='Percentage_Difference')

    # Save results to Excel
    results_df.to_excel('percentage_difference_results.xlsx', index=False)
    print("Results saved to 'percentage_difference_results.xlsx'")


#----------------------------------------------------------------------------------------------------------------#
# MAIN SECTION OF SKIPRATE SCRIPT 
#----------------------------------------------------------------------------------------------------------------#

# Define the variables for interval selection
start_date = '2023-01-01'  # Example: 'YYYY-MM-DD'
end_date = '2023-02-01'  # Must be the day above the final day you desire

# Collect the dataset using the functions for all BMUs and save results to Excel
bmu_df = bmuid_data_collector()
calculate_and_save_percentage_difference(bmu_df, start_date, end_date)

import pandas as pd
import numpy as np
from database_collector import fpn_data_collector, boalf3_data_collector, abv_data_collector, bmuid_data_collector
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

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
        fpn_df.loc[:, 'interval_start'] = pd.to_datetime(fpn_df['ts']) - timedelta(minutes=15)
        fpn_df.loc[:, 'interval_end'] = pd.to_datetime(fpn_df['ts']) + timedelta(minutes=15)

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

        # Clear interval-related columns and aggregated 'vp' values
        fpn_df.drop(columns=['interval_start', 'interval_end', 'vp'], inplace=True)

        return total_vol, total_vp, percentage_difference

    except Exception as e:
        print(f'Error in percentage_difference function: {e}')
        return 0, 0, 0  # Return default values in case of an error

#----------------------------------------------------------------------------------------------------------------#

def monthly_percentage_difference(bmu_df, start_month, end_month):
    # Filter out BMU IDs starting with 'C'
    bmu_df = bmu_df[~bmu_df['id'].str.startswith('C')]

    # Create a new Excel writer for all months
    with pd.ExcelWriter('percentage_difference_results.xlsx', engine='openpyxl') as writer:
        current_month = start_month
        while current_month <= end_month:
            # Determine start and end dates for the current month
            start_date = current_month.strftime('%Y-%m-01')
            end_date = (current_month + relativedelta(months=1)).strftime('%Y-%m-01')

            # Create an empty DataFrame to store results for this month
            results_df = pd.DataFrame(columns=['BMU_ID', 'Total_VOL', 'Total_VP', 'Percentage_Difference'])

            for index, row in bmu_df.iterrows():
                bmu_id = row['id']  # Change 'id' to the actual column name in your DataFrame

                # Collect the dataset using the functions for the BMU
                fpn_df = fpn_data_collector(start_date, end_date, bmu_id)
                boalf_df = boalf3_data_collector(start_date, end_date, bmu_id)
                abv_df = abv_data_collector(start_date, end_date, bmu_id)
                abv_df['vol'] = abv_df['vol'] * 2  # Counteract the MWh values of the real generation

                # Check if any of the data frames is empty, skip BMU if true
                missing_data = []
                if fpn_df.empty:
                    missing_data.append('FPN')
                if boalf_df.empty:
                    missing_data.append('BOALF')
                if abv_df.empty:
                    missing_data.append('ABV')

                if missing_data:
                    print(f'Skipping BMU {bmu_id} for {current_month} due to missing data: {", ".join(missing_data)}.')
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

            # Write the DataFrame to the Excel sheet for this month
            sheet_name = current_month.strftime('%Y-%m')
            results_df.to_excel(writer, index=False, sheet_name=sheet_name)

            print(f"Results for {sheet_name} saved to 'percentage_difference_results.xlsx'")

            current_month += relativedelta(months=1)

#----------------------------------------------------------------------------------------------------------------#
# MAIN SECTION OF SKIPRATE SCRIPT 
#----------------------------------------------------------------------------------------------------------------#

# Define the variables for month selection
start_month = datetime.strptime('2021-01-01', '%Y-%m-%d').date()
end_month = datetime.strptime('2021-02-01', '%Y-%m-%d').date()

# Collect the dataset using the functions for all BMUs and save results to Excel
bmu_df = bmuid_data_collector()
monthly_percentage_difference(bmu_df, start_month, end_month)

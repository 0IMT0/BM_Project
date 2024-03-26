import pandas as pd
from database_collector import boav2_data_collector

#----------------------------------------------------------------------------------------------------------------#
# FUNCTIONS
#----------------------------------------------------------------------------------------------------------------#

def calculate_curtailment(ct_df):
    # Sum up the values of the 'bv' column to get the curtailment volume
    print(ct_df)
    curtailment_value = round(ct_df['bv'].sum(), 2)
    return curtailment_value

def print_monthly_curtailment(start_date, end_date):
    # Check if the difference between start_date and end_date is less than a month
    if (pd.to_datetime(end_date) - pd.to_datetime(start_date)) < pd.DateOffset(months=1):
        # If the difference is less than a month, calculate curtailment for that period
        ct_df = boav2_data_collector(start_date, end_date)
        curtailment_value = calculate_curtailment(ct_df)
        print(f'Curtailment Volume ({start_date} to {end_date}): {curtailment_value} MWh')
    else:
        # Create an empty list to store monthly curtailment values
        monthly_curtailment_data = []

        # Get the end month from the end date
        end_month = pd.to_datetime(end_date).strftime('%Y-%m')

        # Iterate through each month of the specified period
        for month in pd.date_range(start=start_date, end=end_date, freq='MS'):
            # Skip the iteration if the current month is the same as the end date month
            if month.strftime('%Y-%m') == end_month:
                continue
            
            month_end = month + pd.offsets.MonthBegin(1)
            month_end = month_end.strftime('%Y-%m-%d')
            
            # Collect data for the current month
            ct_df = boav2_data_collector(month.strftime('%Y-%m-%d'), month_end)
            
            # Call the calculate_curtailment function with the provided DataFrame and time frame
            curtailment_value = calculate_curtailment(ct_df)
            
            # Append the monthly curtailment data to the list
            monthly_curtailment_data.append({'Curtailment Volume (MWh)': curtailment_value})

        # Convert the list of dictionaries into a DataFrame
        monthly_curtailment_df = pd.DataFrame(monthly_curtailment_data)

        # Print the monthly curtailment DataFrame without index
        print(monthly_curtailment_df.to_string(index=False))

#----------------------------------------------------------------------------------------------------------------#
# MAIN SECTION OF Curtailment Analyser SCRIPT 
#----------------------------------------------------------------------------------------------------------------#

start_date = '2023-12-25'
end_date = '2023-12-26'

# Choose whether to print monthly curtailment or total curtailment for the specified period
print_monthly = True  # Change to True if you want to print monthly curtailment

if print_monthly:
    print_monthly_curtailment(start_date, end_date)
else:
    # Collect data for the provided start date and end date
    ct_df = boav2_data_collector(start_date, end_date)
    
    # Call the calculate_curtailment function with the provided DataFrame and time frame
    curtailment_value = calculate_curtailment(ct_df)
    
    # Print the curtailment volume for the provided time frame
    print(f'Curtailment Volume ({start_date} to {end_date}): {curtailment_value} MWh')

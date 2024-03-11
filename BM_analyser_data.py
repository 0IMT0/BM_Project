import pandas as pd
from database_collector import boav_data_collector, boalf2_data_collector, ebocf_data_collector
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta 

#----------------------------------------------------------------------------------------------------------------#
# FUNCTIONS
#----------------------------------------------------------------------------------------------------------------#

def calculate_total_volume(boav_df):
    # Check if the required columns are present in the DataFrame
    if 'ov' not in boav_df.columns or 'bv' not in boav_df.columns:
        raise ValueError("DataFrame should have 'ov' and 'bv' columns")

    # Calculate total ov and bv values
    total_ov = boav_df['ov'].sum()
    total_bv = boav_df['bv'].sum()

    # Calculate final cost by adding ov and bv
    final_volume = total_ov + total_bv

    return total_ov, total_bv, final_volume

#----------------------------------------------------------------------------------------------------------------#

def calculate_total_cost(ebocf_df):
    # Check if the required columns are present in the DataFrame
    if 'oc' not in ebocf_df.columns or 'bc' not in ebocf_df.columns:
        raise ValueError("DataFrame should have 'oc' and 'bc' columns")

    # Calculate total oc and bc values
    total_oc = ebocf_df['oc'].sum()
    total_bc = ebocf_df['bc'].sum()

    # Calculate final cost by adding oc and bc
    final_cost_ebocf = total_oc + total_bc

    return total_oc, total_bc, final_cost_ebocf

#----------------------------------------------------------------------------------------------------------------#

def count_bids_offers(boalf2_df):
    # Check if the DataFrame is not empty
    if boalf2_df.empty:
        raise ValueError("DataFrame is empty")

    # Count the number of rows in the DataFrame
    total_rows = len(boalf2_df)

    return total_rows

#----------------------------------------------------------------------------------------------------------------#

def save_to_excel(data):
    # Create a DataFrame with the data
    df = pd.DataFrame(data)

    # Save DataFrame to Excel file
    file_name = f"BM_analysis.xlsx"
    df.to_excel(file_name)
    print(f"Data saved to {file_name}")

#----------------------------------------------------------------------------------------------------------------#

def generate_monthly_date_ranges(start_year, start_month, end_year, end_month):
    # Define start and end dates
    start_date = datetime(start_year, start_month, 1)
    end_date = datetime(end_year, end_month, 1)

    # Initialize an empty list to store date ranges
    date_ranges_with_time = []
    date_ranges_without_time = []

    # Loop through each month from start_year/start_month to end_year/end_month
    while start_date <= end_date:
        # Calculate the end date of the current month
        end_of_month = start_date.replace(day=1) + relativedelta(months=1) - timedelta(days=1)

        # Append start and end date of the current month with time to date_ranges_with_time
        date_ranges_with_time.append((start_date.strftime('%Y-%m-%d 00:00'), end_of_month.strftime('%Y-%m-%d 23:59')))

        # Append start and end date of the current month without time to date_ranges_without_time
        date_ranges_without_time.append((start_date.strftime('%Y-%m-%d'), end_of_month.strftime('%Y-%m-%d')))

        # Move to the start of the next month
        start_date = end_of_month + timedelta(days=1)

    return date_ranges_with_time, date_ranges_without_time


#----------------------------------------------------------------------------------------------------------------#
# MAIN SECTION OF SKIPRATE SCRIPT 
#----------------------------------------------------------------------------------------------------------------#

date_ranges_with_time, date_ranges_without_time = generate_monthly_date_ranges(2020, 1, 2024, 2)

# Initialize a list to store all the data
BM_data = []

for i, (start_date_with_time, end_date_with_time) in enumerate(date_ranges_with_time):
    start_date_without_time, end_date_without_time = date_ranges_without_time[i]
    print()
    print(f"{start_date_without_time} to {end_date_without_time}")

    # Collect data with start and end dates with/without time
    boav_df = boav_data_collector(start_date_without_time, end_date_without_time)
    ebocf_df = ebocf_data_collector(start_date_without_time, end_date_without_time)
    boalf2_df = boalf2_data_collector(start_date_with_time, end_date_with_time)

    # Volume outputs (MWh)
    total_ov, total_bv, final_cost = calculate_total_volume(boav_df)
    print(f"Total ov value: {round(total_ov, 2)}")
    print(f"Total bv value: {round(total_bv, 2)}")
    print(f"Final cost: {round(final_cost, 2)}")

    # Cost outputs
    total_oc, total_bc, final_cost_ebocf = calculate_total_cost(ebocf_df)
    print(f"Total oc value: {round(total_oc, 2)}")
    print(f"Total bc value: {round(total_bc, 2)}")
    print(f"Final cost: {round(final_cost_ebocf, 2)}")

    # Activity outputs
    total_BOD = count_bids_offers(boalf2_df)
    print(f"The total number of B&O = {total_BOD}")

    # Append data to the list
    BM_data.append({
        'Start Date': start_date_without_time,
        'End Date': end_date_without_time,
        'Total OV Value': round(total_ov, 2),
        'Total BV Value': round(total_bv, 2),
        'Final Volume': round(final_cost, 2),
        'Total OC Value': round(total_oc, 2),
        'Total BC Value': round(total_bc, 2),
        'Final Cost': round(final_cost_ebocf, 2), 
        'Total # B&O': total_BOD
    })

# Save all data to Excel
save_to_excel(BM_data)

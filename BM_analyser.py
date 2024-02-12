import pandas as pd
from database_collector import boav_data_collector, boalf2_data_collector
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta  # Add this import

#----------------------------------------------------------------------------------------------------------------#
# FUNCTIONS
#----------------------------------------------------------------------------------------------------------------#

def calculate_total_cost(boav_df):
    # Check if the required columns are present in the DataFrame
    if 'ov' not in boav_df.columns or 'bv' not in boav_df.columns:
        raise ValueError("DataFrame should have 'ov' and 'bv' columns")

    # Calculate total ov and bv values
    total_ov = boav_df['ov'].sum()
    total_bv = boav_df['bv'].sum()

    # Calculate final cost by adding ov and bv
    final_cost = total_ov + total_bv

    return total_ov, total_bv, final_cost

def count_bids_offers(boalf2_df):
    # Check if the DataFrame is not empty
    if boalf2_df.empty:
        raise ValueError("DataFrame is empty")

    # Count the number of rows in the DataFrame
    total_rows = len(boalf2_df)

    return total_rows

def save_to_excel(data):
    # Create a DataFrame with the data
    df = pd.DataFrame(data)

    # Save DataFrame to Excel file
    file_name = f"BM_analysis.xlsx"
    df.to_excel(file_name)
    print(f"Data saved to {file_name}")

def generate_monthly_date_ranges(start_year, start_month, end_year, end_month):
    # Define start and end dates
    start_date = datetime(start_year, start_month, 1)
    end_date = datetime(end_year, end_month, 1)

    # Initialize an empty list to store date ranges
    date_ranges = []

    # Loop through each month from start_year/start_month to end_year/end_month
    while start_date <= end_date:
        # Calculate the end date of the current month
        end_of_month = start_date.replace(day=1) + relativedelta(months=1) - timedelta(days=1)

        # Append start and end date of the current month to date_ranges
        date_ranges.append((start_date.strftime('%Y-%m-%d 00:00'), end_of_month.strftime('%Y-%m-%d 23:59')))

        # Move to the start of the next month
        start_date = end_of_month + timedelta(days=1)

    return date_ranges


#----------------------------------------------------------------------------------------------------------------#
# MAIN SECTION OF SKIPRATE SCRIPT 
#----------------------------------------------------------------------------------------------------------------#

date_ranges = generate_monthly_date_ranges(2020, 1, 2024, 1) # (start year, start month, end year, end month)

# Initialize a list to store all the data
all_data = []

for i, (start_date, end_date) in enumerate(date_ranges):
    print()
    print(f"{start_date} to {end_date}")

    boav_df = boav_data_collector(start_date, end_date)
    boalf2_df = boalf2_data_collector(start_date, end_date)

    # Cost outputs
    total_ov, total_bv, final_cost = calculate_total_cost(boav_df)
    print(f"Total ov value: {round(total_ov, 2)}")
    print(f"Total bv value: {round(total_bv, 2)}")
    print(f"Final cost: {round(final_cost, 2)}")

    # Activity outputs
    total_BOD = count_bids_offers(boalf2_df)
    print(f"The total number of B&O = {total_BOD}")

    # Append data to the list
    all_data.append({
        'Start Date': start_date,
        'End Date': end_date,
        'Total OV Value': round(total_ov, 2),
        'Total BV Value': round(total_bv, 2),
        'Final Cost': round(final_cost, 2),
        'Total B&O': total_BOD
    })

# Save all data to Excel
save_to_excel(all_data)

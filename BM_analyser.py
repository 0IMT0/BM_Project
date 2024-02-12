import pandas as pd
from database_collector import boav_data_collector, boalf2_data_collector

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

#----------------------------------------------------------------------------------------------------------------#
# MAIN SECTION OF SKIPRATE SCRIPT 
#----------------------------------------------------------------------------------------------------------------#

start_date = '2023-01-01 00:00'
end_date = '2023-01-31 23:59'

boav_df = boav_data_collector(start_date, end_date)
boalf2_df = boalf2_data_collector(start_date, end_date)

# Cost outputs
total_ov, total_bv, final_cost = calculate_total_cost(boav_df)
print(f"Total ov value: {total_ov}")
print(f"Total bv value: {total_bv}")
print(f"Final cost: {final_cost}")

# Activity outputs
total_BOD = count_bids_offers(boalf2_df)
print(f"The total number of BOD = {total_BOD}")
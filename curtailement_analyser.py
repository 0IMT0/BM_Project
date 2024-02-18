import pandas as pd
from database_collector import boav2_data_collector

#----------------------------------------------------------------------------------------------------------------#
# FUNCTIONS
#----------------------------------------------------------------------------------------------------------------#

def calculate_curtailment(ct_df):
    
    # Sum up the values of the 'bv' column to get the curtailment volume
    curtailment_value = round(ct_df['bv'].sum(),2)
    
    return curtailment_value

#----------------------------------------------------------------------------------------------------------------#
# MAIN SECTION OF Curtailment Analyser SCRIPT 
#----------------------------------------------------------------------------------------------------------------#

start_date = '2021-01-01'
end_date = '2023-04-01'

# Collect data
ct_df = boav2_data_collector(start_date, end_date)

# Call the calculate_curtailment function with the provided DataFrame and time frame
curtailment_value = calculate_curtailment(ct_df)

print(f'Curtailment Volume ({start_date} to {end_date}): {curtailment_value} MWh')

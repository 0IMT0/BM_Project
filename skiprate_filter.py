
import pandas as pd
from datetime import datetime
from database_collector import boalf_data_collector, bod_data_collector, offers_data_collector, bids_data_collector, mel_data_collector, mil_data_collector, fpn_data_collector
    
#----------------------------------------------------------------------------------------------------------------#
# FUNCTIONS 
#----------------------------------------------------------------------------------------------------------------#

def update_offers(offers_df, mel_df, fpn_df):
    # Merge ve values from mel_df
    if 'mel_ve' not in offers_df.columns:
        offers_df = pd.merge(offers_df, mel_df[['bmu_id', 've']], left_on='id', right_on='bmu_id', how='left').drop(columns=['bmu_id']).rename(columns={'ve': 'mel_ve'}).drop_duplicates() 
    # Merge vp values from fpn_df
    if 'fpn_vp' not in offers_df.columns:
        offers_df = pd.merge(offers_df, fpn_df[['bmu_id', 'vp']], left_on='id', right_on='bmu_id', how='left').drop(columns=['bmu_id']).rename(columns={'vp': 'fpn_vp'}).drop_duplicates()
    return offers_df
    
def update_bids(bids_df, mil_df, fpn_df):
    # Merge vf values from mil_df
    if 'mil_vf' not in bids_df.columns:
        bids_df = pd.merge(bids_df, mil_df[['bmu_id', 'vf']], left_on='id', right_on='bmu_id', how='left').drop(columns=['bmu_id']).rename(columns={'vf': 'mil_vf'}).drop_duplicates()
    # Merge vp values from fpn_df
    if 'fpn_vp' not in bids_df.columns:
        bids_df = pd.merge(bids_df, fpn_df[['bmu_id', 'vp']], left_on='id', right_on='bmu_id', how='left').drop(columns=['bmu_id']).rename(columns={'vp': 'fpn_vp'}).drop_duplicates()
    return bids_df

def datetime_to_string(df):
    # List of specific columns to convert to string, or else you cannot export to an excel.
    columns_to_convert = ['ts', 'ta', 'ts1', 'ts2']

    for col in columns_to_convert:
        if col in df.columns:
            # ERROR TESTING: print(f"Converting '{col}' column to string to remove timezone information.")
            df[col] = df[col].astype(str)
    return df

#----------------------------------------------------------------------------------------------------------------#
# MAIN SECTION OF SKIPRATE SCRIPT 
#----------------------------------------------------------------------------------------------------------------#

#PLEASE INSERT the date/times you would like to inspect (YYYY-MM-DD hh:mm)
date_str_list = [
    '2023-01-18 03:00',
    '2023-01-18 12:00',
    '2024-01-17 03:00',
    '2024-01-17 12:00', 
    '2023-09-27 12:00', # Windy day (storm Agnes)
    '2023-03-05 12:00', # None-windy day 
    # Add more dates as needed
]

for date_str in date_str_list:
    print(date_str)
    # Apply timezone conversion to DataFrames
    boalf_df = datetime_to_string(boalf_data_collector(date_str))
    bod_df = datetime_to_string(bod_data_collector(date_str))
    offers_df = datetime_to_string(offers_data_collector(date_str))
    bids_df = datetime_to_string(bids_data_collector(date_str))
    mel_df = datetime_to_string(mel_data_collector(date_str))
    mil_df = datetime_to_string(mil_data_collector(date_str))
    fpn_df = datetime_to_string(fpn_data_collector(date_str))

    # Apply the transformation
    updated_offers_df = update_offers(offers_df, mel_df, fpn_df)
    updated_bids_df = update_bids(bids_df, mil_df, fpn_df)

    # Format the filename with the current date
    date_name = datetime.strptime(date_str, '%Y-%m-%d %H:%M')
    formatted_date_str = date_name.strftime('%Y-%m-%d_%H%M')
    excel_file_path = f'{formatted_date_str}.xlsx'

    with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
        boalf_df.to_excel(writer, sheet_name='boalf', index=False)
        bod_df.to_excel(writer, sheet_name='bod', index=False)
        updated_offers_df.to_excel(writer, sheet_name='offers', index=False)
        updated_bids_df.to_excel(writer, sheet_name='bids', index=False)
        mel_df.to_excel(writer, sheet_name='mel', index=False)
        mil_df.to_excel(writer, sheet_name='mil', index=False)
        fpn_df.to_excel(writer, sheet_name='fpn', index=False)

    print(f"Data successfully written to {excel_file_path}")

#----------------------------------------------------------------------------------------------------------------#
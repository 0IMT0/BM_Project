from database_access import database_login
from date_time_GUI import create_date_selector
import pandas as pd

def boalf_data_collector():
    # Get the selected start date, end date, and market type from the GUI
    start_date, end_date, market_type = create_date_selector()
    print(f"Start Date: {start_date}, End Date: {end_date}, Market Type: {market_type}")

    # SQL query with the WHERE clause for the specified time frame
    sql_query = f"""
    SELECT id, ts, va, boalf_id 
    FROM public.bmra_boalflevel
    WHERE ts >= '{start_date}' AND ts < '{end_date}';
    """

    # Execute SQL query and read the data into a DataFrame
    boalf_data = pd.read_sql(sql_query, database_login())
    # Display the filtered DataFrame
    print(boalf_data)


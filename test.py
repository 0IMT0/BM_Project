from database_access import database_login
import pandas as pd

# Specify the date for filtering
specified_date1 = "2023-11-12 00:00:00+00:00"
specified_date2 = "2023-11-13 00:00:00+00:00"

# Your SQL query with the WHERE clause for the specified date
sql_query_1 = f"""
SELECT id, ts, va, boalf_id 
FROM public.bmra_boalflevel
WHERE ts >= '{specified_date1}' AND ts < '{specified_date2}';
"""

# Execute your SQL query and read the data into a DataFrame
boalf_data = pd.read_sql(sql_query_1, database_login())

print(boalf_data)  # Display the filtered DataFrame




def bod_data_collector():
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
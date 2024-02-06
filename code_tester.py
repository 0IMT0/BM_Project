import pandas as pd
# Assuming database_login is defined and imports correctly

def boalf_data_collector(date_str):
    """
    Fetches data for a specified date and ensures certain datetime columns are treated as strings.

    Parameters:
    - date_str (str): The date for which to collect data, in a string format.

    Returns:
    - pd.DataFrame: The collected data with specified columns as strings.
    """

    # SQL query with the WHERE clause for the specified time frame
    sql_bmra_boalf = f"""
    SELECT bmra_boalf.id, bmra_boalflevel.ts, bmra_boalflevel.va, bmra_boalf.ts AS "ts(1)", bmra_boalf.ta, bmra_boalf.bmu_id, bmra_bmu.name, bmra_bmu.type_id 
    FROM bmra_boalflevel
    LEFT JOIN bmra_boalf ON bmra_boalf.id = bmra_boalflevel.boalf_id
    LEFT JOIN bmra_bmu ON bmra_boalf.bmu_id = bmra_bmu.id
    WHERE bmra_boalflevel.ts = '{date_str}'
    ORDER BY bmra_boalflevel.ts;
    """

    # Define the data types for the columns you want to import as strings
    dtype_dict = {
        'ts': str,
        'ts(1)': str,  # Assuming you meant this as an example. Adjust if you have an actual column named differently.
        'ta': str
    }

    # Execute SQL query and read the data into a DataFrame, specifying column data types
    boalf_data = pd.read_sql(sql=sql_bmra_boalf, con=database_login(), dtype=dtype_dict)

    # Display the filtered DataFrame
    print(boalf_data)

    return boalf_data

date_str = '2023-01-18 03:00'

boalf_data_collector(date_str)
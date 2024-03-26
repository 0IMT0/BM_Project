import pandas as pd
from database_access import database_login

#----------------------------------------------------------------------------------------------------------------#
# FUNCTIONS
#----------------------------------------------------------------------------------------------------------------#

def print_battery_volume(start_date, end_date):
    # If start_date and end_date are a year apart, perform yearly analysis
    if pd.to_datetime(end_date) - pd.to_datetime(start_date) >= pd.Timedelta(days=365):
        # Define the SQL query for fetching battery data within the provided year
        sql_query = f"""
        select bmra_boav.ts, bmra_boav.nn, bmra_boav.ov, bmra_boav.bv, bmra_boav.bmu_id, bmra_bmu.type_id
            from bmra_boav
        left join bmra_bmu
            on bmra_bmu.id = bmra_boav.bmu_id
        where bmra_boav.ts >= '{start_date}'
            and bmra_boav.ts < '{end_date}'
            and bmra_bmu.type_id = 'BATT'
        order by bmra_boav.ts;
        """
        
        # Fetch data from the database using the provided SQL query
        boalf_data = pd.read_sql(sql_query, database_login())

        # Remove duplicate rows based on 'ts' and keep the last row
        boalf_data = boalf_data.drop_duplicates(subset=['ts'], keep='last')

        # Count the number of batteries and rows
        num_batteries = boalf_data['bmu_id'].nunique()
        num_rows = boalf_data.shape[0]

        # Calculate battery power distribution total and battery consumption for the whole year
        battery_power_distribution_total = boalf_data[boalf_data['nn'] > 0]['ov'].sum()
        battery_consumption = abs(boalf_data[boalf_data['nn'] < 0]['bv'].sum())

        # Print the yearly battery count
        print(f"Number of batteries instructed ({start_date} to {end_date}): {num_batteries}")
        print(f"Number of instructions: {num_rows}")
        print(f"Yearly Battery Power Distribution Total: {battery_power_distribution_total}")
        print(f"Yearly Battery Consumption: {battery_consumption}")
    
    else:  # Perform monthly analysis
        # Create an empty list to store monthly battery count values
        monthly_battery_count_data = []

        # Iterate through each month of the specified period
        for month in pd.date_range(start=start_date, end=end_date, freq='MS'):
            month_end = month + pd.offsets.MonthBegin(1)
            month_end = month_end.strftime('%Y-%m-%d')
            
            # Define the SQL query for fetching battery data within the current month
            sql_bmra_boalf = f"""
            select bmra_boav.ts, bmra_boav.nn, bmra_boav.ov, bmra_boav.bv, bmra_boav.bmu_id, bmra_bmu.type_id
                from bmra_boav
            left join bmra_bmu
                on bmra_bmu.id = bmra_boav.bmu_id
            where bmra_boav.ts >= '{month.strftime('%Y-%m-%d')}'
                and bmra_boav.ts < '{month_end}'
                and bmra_bmu.type_id = 'BATT'
            order by bmra_boav.ts;
            """

            # Fetch data from the database using the provided SQL query
            boalf_data_monthly = pd.read_sql(sql_bmra_boalf, database_login())

            # Count the number of batteries and rows for the current month
            num_batteries = boalf_data_monthly['bmu_id'].nunique()
            num_rows = boalf_data_monthly.shape[0]

            # Calculate battery power distribution total and battery consumption for the current month
            battery_power_distribution_total = boalf_data_monthly[boalf_data_monthly['nn'] > 0]['ov'].sum()
            battery_consumption = abs(boalf_data_monthly[boalf_data_monthly['nn'] < 0]['bv'].sum())
            
            # Append the monthly battery count data to the list
            monthly_battery_count_data.append({'Month': month.strftime('%Y-%m'), 'Number of Batteries': num_batteries,
                                               'Number of Instructions': num_rows,
                                               'Monthly Battery Distribution (MWh)': battery_power_distribution_total,
                                               'Monthly Battery Consumption (MWh)': battery_consumption})

        # Convert the list of dictionaries into a DataFrame
        monthly_battery_count_df = pd.DataFrame(monthly_battery_count_data)

        # Print the monthly battery count DataFrame without index
        print(monthly_battery_count_df.to_string(index=False))

#----------------------------------------------------------------------------------------------------------------#
# MAIN SECTION OF SCRIPT
#----------------------------------------------------------------------------------------------------------------#

start_date = "2024-01-01"
end_date = "2024-12-01" 

print_battery_volume(start_date, end_date)



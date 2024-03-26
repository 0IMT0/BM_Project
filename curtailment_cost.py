from database_access import database_login
import pandas as pd

start_date = "2021-01-01"
end_date = "2022-01-01"

sql_bmra_ebocf = f"""
select bmra_ebocf.sd, bmra_ebocf.bc, bmra_ebocf.bmu_id 
    from bmra_ebocf
inner join bmra_bmu
    on bmra_bmu.id = bmra_ebocf.bmu_id
where bmra_ebocf.sd >= '{start_date}'
    and bmra_ebocf.sd < '{end_date}'
    and (bmra_bmu.type_id = 'WON' or bmra_bmu.type_id = 'WOFF')
    and bmra_ebocf.nn < 1
order by bmra_ebocf.sd, bmra_ebocf.sp;
"""

ebocf_data = pd.read_sql(sql_bmra_ebocf, database_login())

# Convert 'sd' column to datetime format
ebocf_data['sd'] = pd.to_datetime(ebocf_data['sd'])

# Extract month from 'sd' column
ebocf_data['month'] = ebocf_data['sd'].dt.to_period('M')

# Group by month and sum the 'bc' column within each group
monthly_cost = ebocf_data.groupby('month')['bc'].sum()

# Convert to DataFrame with a single column
monthly_cost_df = pd.DataFrame(monthly_cost.values, columns=['Total Cost'])

# Print the DataFrame
print(monthly_cost_df.to_string(index=False))
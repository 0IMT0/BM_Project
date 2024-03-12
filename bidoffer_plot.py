from database_access import database_login
import pandas as pd

# Specify the date for filtering (1 min interval)
start_date = "2023-01-18 15:01:00+00"
end_date = "2023-01-18 15:02:00+00"

# Your SQL query with the WHERE clause for the specified date
sql_bmra_bod = f"""
SELECT*
FROM bmra_bod
WHERE ts >= '{start_date}' AND ts < '{end_date}';
"""
# Execute your SQL query and read the data into a DataFrame
bod_data = pd.read_sql(sql_bmra_bod, database_login())
#print(bod_data)  # Display DataFrame


def plot_bod_1():
    import matplotlib.pyplot as plt
    import pandas as pd

    # Assuming 'nn' is a column in the DataFrame
    under_fpn_data = bod_data[bod_data['nn'] < 0]
    above_fpn_data = bod_data[bod_data['nn'] > 0]

    # Plotting bid-offer curve for 'under FPN'
    plt.scatter(under_fpn_data['vb1'], under_fpn_data['bp'], label='Bid', marker='o')
    plt.scatter(under_fpn_data['vb1'], under_fpn_data['op'], label='Offer', marker='o')

    # Adding labels and title
    plt.xlabel('Volume (MW)')
    plt.ylabel('Price (£/MWh)')
    plt.title('Bid-Offer - Under FPN')
    plt.legend()  # Show legend

    # Display the plot
    plt.grid(True)
    plt.show()

    # Plotting bid-offer curve for 'above FPN'
    plt.scatter(above_fpn_data['vb1'], above_fpn_data['bp'], label='Bid', marker='o')
    plt.scatter(above_fpn_data['vb1'], above_fpn_data['op'], label='Offer', marker='o')

    # Adding labels and title
    plt.xlabel('Volume (MW)')
    plt.ylabel('Price (£/MWh)')
    plt.title('Bid-Offer - Above FPN')
    plt.legend()  # Show legend

    # Display the plot
    plt.grid(True)
    plt.show()


def plot_bod_2():
    import matplotlib.pyplot as plt

    # Assuming 'bod_data' is already loaded with the required data

    # Filter rows where not all values are zero for op, bp, vb1, vb2
    non_zero_rows = bod_data[(bod_data[['op', 'bp', 'vb1', 'vb2']] != 0).all(axis=1)]

    # Plotting the first scatter plot (op vs vb1)
    plt.figure(figsize=(10, 5))
    plt.scatter(non_zero_rows['vb1'], non_zero_rows['op'])
    plt.title('Scatter Plot of op vs vb1')
    plt.xlabel('vb1 (MW)')
    plt.ylabel('op (£/MWh)')
    plt.grid(True)
    plt.show()

    # Plotting the second scatter plot (bp vs vb1)
    plt.figure(figsize=(10, 5))
    plt.scatter(non_zero_rows['vb1'], non_zero_rows['bp'])
    plt.title('Scatter Plot of bp vs vb1')
    plt.xlabel('vb1 (MW)')
    plt.ylabel('bp (£/MWh)')
    plt.grid(True)
    plt.show()


plot_bod_1()
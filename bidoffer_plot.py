from database_access import database_login
import pandas as pd
import os
import matplotlib.pyplot as plt

#----------------------------------------------------------------------------------------------------------------#
# FUNCTIONS
#----------------------------------------------------------------------------------------------------------------#

# Function to check if DataFrame exists in project file
def check_if_df_exists(date, thirty_min):
    file_name_bid = f"SR_{date}_{thirty_min}_bid.pkl"
    file_name_offer = f"SR_{date}_{thirty_min}_offer.pkl"
    return os.path.isfile(file_name_bid) and os.path.isfile(file_name_offer)

def plot_bod_1():
    # Sort bid and offer dataframes by price in ascending order
    bid_data_sorted = bid_data.sort_values(by='bp')
    offer_data_sorted = offer_data.sort_values(by='op')

    # Calculate cumulative volume for bids
    bid_cumulative_volume = bid_data_sorted['vb1'].cumsum()

    # Calculate cumulative volume for offers
    offer_cumulative_volume = offer_data_sorted['vb1'].cumsum()

    # Plot bid-offer curve for 'under FPN' (bids)
    plt.scatter(bid_cumulative_volume, bid_data_sorted['bp'], label='Bid', color='blue')

    # Plot bid-offer curve for 'above FPN' (offers)
    plt.scatter(offer_cumulative_volume, offer_data_sorted['op'], label='Offer', color='red')

    # Adding labels and title
    plt.xlabel('Cumulative Volume (MW)')
    plt.ylabel('Price (£/MWh)')
    plt.title('Bid-Offer Cumulative Volume vs Price')
    plt.legend()  # Show legend

    # Display the plot
    plt.grid(True)
    plt.show()

#----------------------------------------------------------------------------------------------------------------#
# MAIN SECTION OF Curtailment Analyser SCRIPT 
#----------------------------------------------------------------------------------------------------------------#

# Specify the date for filtering (1 min interval)
date = "2023-01-18"
thirty_min = 31

# Check if DataFrame files exist
if check_if_df_exists(date, thirty_min):
    # Load DataFrames from project files
    bid_data = pd.read_pickle(f"SR_{date}_{thirty_min}_bid.pkl")
    offer_data = pd.read_pickle(f"SR_{date}_{thirty_min}_offer.pkl")
else:
    # Bid SQL
    sql_bmra_bod_bid = f"""
    SELECT *
    FROM bmra_bod
    WHERE sd = '{date}'
        AND sp = '{thirty_min}'
        AND nn < 0
        AND NOT (op = 0 AND bp = 0 AND vb1 = 0 AND vb2 = 0);
    """

    # Offer SQL 
    sql_bmra_bod_offer = f"""
    SELECT *
    FROM bmra_bod
    WHERE sd = '{date}'
        AND sp = '{thirty_min}'
        AND nn > 0
        AND NOT (op = 0 AND bp = 0 AND vb1 = 0 AND vb2 = 0);
    """

    # Execute SQL queries and read the data into DataFrames
    bid_data = pd.read_sql(sql_bmra_bod_bid, database_login())
    offer_data = pd.read_sql(sql_bmra_bod_offer, database_login())

    # Save DataFrames to project files
    bid_data.to_pickle(f"SR_{date}_{thirty_min}_bid.pkl")
    offer_data.to_pickle(f"SR_{date}_{thirty_min}_offer.pkl")

# Call the plotting function
plot_bod_1()

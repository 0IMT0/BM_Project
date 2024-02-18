from database_collector import fpn_data_collector, boalf3_data_collector
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons

# Define the variables for interval selection and BMU IDs
start_date = '2023-01-01'  # Example: 'YYYY-MM-DD'
end_date = '2023-01-02'  # Example: 'YYYY-MM-DD'
bmu1 = 'E_MOYEW-1'  # Example: 'E_MOYEW-1'
bmu2 = 'C__PSTAT011'  # Example: 'C__PSTAT011'

# Function to create plot for BMU comparison
def BMU_plot_comparator(fpn_df1, fpn_df2, boalf_df1, boalf_df2, bmu1, bmu2):
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.subplots_adjust(left=0.2)

    lines = []
    labels = []

    # Plot BMU 1 data
    if not fpn_df1.empty:
        line1, = ax.plot(fpn_df1['ts'], fpn_df1['vp'], marker='o', label=f'BMU {bmu1} - Final Physical Notification')
        lines.append(line1)
        labels.append(f'BMU {bmu1} - Final Physical Notification')

    if not boalf_df1.empty:
        line2, = ax.plot(boalf_df1['ts'], boalf_df1['va'], marker='o', label=f'BMU {bmu1} - BOALF', color='orange')
        lines.append(line2)
        labels.append(f'BMU {bmu1} - BOALF')

    # Plot BMU 2 data
    if not fpn_df2.empty:
        line3, = ax.plot(fpn_df2['ts'], fpn_df2['vp'], marker='o', label=f'BMU {bmu2} - Final Physical Notification')
        lines.append(line3)
        labels.append(f'BMU {bmu2} - Final Physical Notification')

    if not boalf_df2.empty:
        line4, = ax.plot(boalf_df2['ts'], boalf_df2['va'], marker='o', label=f'BMU {bmu2} - BOALF', color='green')
        lines.append(line4)
        labels.append(f'BMU {bmu2} - BOALF')

    ax.legend(lines, labels, loc='upper left')  # Adjust legend position
    ax.set_title('Time vs MW Plot for BMUs')
    ax.set_xlabel('Time')
    ax.set_ylabel('MW Values')
    ax.tick_params(axis='x', rotation=90)

    # Add a toggle button
    ax_toggle = plt.axes([0.02, 0.5, 0.1, 0.06])  # Adjust position of toggle box within the figure
    check = CheckButtons(ax_toggle, ['BMU1', 'BMU2'], [True, True])

    def toggle_func(label):
        if label == 'BMU1':
            for line in lines:
                if 'BMU E_MOYEW-1' in line.get_label():
                    line.set_visible(not line.get_visible())
        elif label == 'BMU2':
            for line in lines:
                if 'BMU C__PSTAT011' in line.get_label():
                    line.set_visible(not line.get_visible())
        plt.draw()

    check.on_clicked(toggle_func)

    plt.show()

# Collect the dataset using the function from database_collector.py for both BMUs
fpn_df1 = fpn_data_collector(start_date, end_date, bmu1)
fpn_df2 = fpn_data_collector(start_date, end_date, bmu2)
boalf_df1 = boalf3_data_collector(start_date, end_date, bmu1)
boalf_df2 = boalf3_data_collector(start_date, end_date, bmu2)

# Create plot for BMU comparison
BMU_plot_comparator(fpn_df1, fpn_df2, boalf_df1, boalf_df2, bmu1, bmu2)

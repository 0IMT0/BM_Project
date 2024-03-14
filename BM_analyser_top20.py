import pandas as pd
from database_collector import boalf_an_data_collector

start_date = '2024-01-01'
end_date = '2024-03-01'

boalf_df = boalf_an_data_collector(start_date, end_date)

# Count occurrences of each bmu_id
bmu_id_counts = boalf_df['bmu_id'].value_counts()

# Display the top 5 results
print("Top 20 BMU_ID   Count")
print("----------------------")
for bmu_id, count in bmu_id_counts.head(20).items():
    print(f"{bmu_id}      {count}")

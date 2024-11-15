import numpy as np
import pandas as pd
import json

crime = pd.read_csv("../_DATASET/17_Crime_by_place_of_occurrence_2001_2012.csv")

# Sum the specified columns and replace them with new columns
crime['RESIDENTIAL PREMISES'] = crime.iloc[:, 2:6].sum(axis=1)
crime['HIGHWAYS'] = crime.iloc[:, 6:10].sum(axis=1)
crime['RIVER and SEA'] = crime.iloc[:, 10:14].sum(axis=1)
crime['RAILWAYS'] = crime.iloc[:, 14:18].sum(axis=1)
crime['BANKS'] = crime.iloc[:, 18:22].sum(axis=1)
crime['COMMERCIAL ESTABLISHMENTS'] = crime.iloc[:, 22:26].sum(axis=1)
crime['OTHER PLACES'] = crime.iloc[:, 26:30].sum(axis=1)
crime['TOTAL'] = crime.iloc[:, 30:34].sum(axis=1)

# Drop the original columns that were summed
crime.drop(columns=crime.columns[2:34], inplace=True)

# Filter out rows where 'STATE/UT' contains 'TOTAL' in any case
crime = crime[~crime['STATE/UT'].str.contains("TOTAL", case=False)]

states_rto = {
    "ARUNACHAL PRADESH": "ar",
    "ANDHRA PRADESH": "ap",
    "ASSAM": "as",
    "BIHAR": "br",
    "CHHATTISGARH": "cg",
    "GUJARAT": "gj",
    "GOA": "ga",
    "HIMACHAL PRADESH": "hp",
    "HARYANA": "hr",
    "JHARKHAND": "jh",
    "JAMMU & KASHMIR": "jk",
    "KERALA": "kl",
    "KARNATAKA": "ka",
    "MAHARASHTRA": "mh",
    "MANIPUR": "mn",
    "MADHYA PRADESH": "mp",
    "MIZORAM": "mz",
    "MEGHALAYA": "ml",
    "NAGALAND": "nl",
    "ODISHA": "od",
    "PUNJAB": "pb",
    "RAJASTHAN": "rj",
    "SIKKIM": "sk",
    "TAMIL NADU": "tn",
    "TRIPURA": "tp",
    "UTTAR PRADESH": "up",
    "UTTARAKHAND": "uk",
    "WEST BENGAL": "wb",
    "A & N ISLANDS": "an",
    "CHANDIGARH": "ch",
    "DAMAN & DIU": "dd",
    "D & N HAVELI": "dn",
    "LAKSHADWEEP": "ld",
    "DELHI": "dl",
    "PUDUCHERRY": "py"
}

yearwise_statewise_total = crime.groupby(['STATE/UT', 'YEAR']).agg({
    'RESIDENTIAL PREMISES': 'sum',
    'HIGHWAYS': 'sum',
    'RIVER and SEA': 'sum',
    'RAILWAYS': 'sum',
    'BANKS': 'sum',
    'COMMERCIAL ESTABLISHMENTS': 'sum',
    'OTHER PLACES': 'sum',
    'TOTAL': 'sum'
}).reset_index()

# Initialize lists for labels, parents, and values
labels = []
parents = []
values = []

# Root node
root_value = crime['TOTAL'].sum()
labels.append("India Total Crimes")
parents.append("")
values.append(root_value)

# Loop through each year
for year in sorted(crime['YEAR'].unique()):
    # Add year node
    year_total = crime[crime['YEAR'] == year]['TOTAL'].sum()
    labels.append(f"Year {year}")
    parents.append("India Total Crimes")
    values.append(year_total)

    # Loop through each STATE/UT for the year
    for state in crime[crime['YEAR'] == year]['STATE/UT'].unique():
        state_data = crime[(crime['YEAR'] == year) & (crime['STATE/UT'] == state)]
        # print(state_data)
        state_total = state_data['TOTAL'].values[0]
        
        # Add state node under year
        labels.append(state + "_" + str(year)[-2:])
        parents.append(f"Year {year}")
        values.append(state_total)
        
        # Add place nodes under state
        for place in ['RESIDENTIAL PREMISES', 'HIGHWAYS', 'RIVER and SEA', 
                      'RAILWAYS', 'BANKS', 'COMMERCIAL ESTABLISHMENTS', 'OTHER PLACES']:
            place_value = state_data[place].values[0]
            labels.append(f"{place}_{states_rto[state]}{str(year)[-2:]}")
            parents.append(state + "_" + str(year)[-2:])
            values.append(place_value)

# Convert values to Python native types (to handle numpy.int64)
values = [int(value) for value in values]

# Create the JSON object
treemap_data = {
    "labels": labels,
    "parents": parents,
    "values": values
}

# Write the JSON object to a JavaScript file
with open('../_TREEMAP_DATA/treemap_crime_rate_place.js', 'w') as f:
    f.write(f"const treemapData = {json.dumps(treemap_data)};")

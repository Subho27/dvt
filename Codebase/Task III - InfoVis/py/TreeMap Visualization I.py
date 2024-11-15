import numpy as np
import pandas as pd
import json

crime = pd.read_csv("../_DATASET/01_District_wise_crimes_committed_IPC_2001_2012.csv")

crime_filtered = crime.drop(columns='YEAR').groupby(['STATE/UT', 'DISTRICT']).sum().reset_index()
crime_filtered = crime_filtered[~crime_filtered['DISTRICT'].isin(['TOTAL', 'DELHI UT TOTAL'])]

# Dropping specified columns
crime_filtered.drop(columns=[
    'CUSTODIAL RAPE', 'OTHER RAPE', 'KIDNAPPING AND ABDUCTION OF WOMEN AND GIRLS',
    'KIDNAPPING AND ABDUCTION OF OTHERS', 'AUTO THEFT', 'OTHER THEFT'
], inplace=True)

# Summing all remaining crime columns for each row and adding as a new column "CRIME"
crime_filtered['TOTAL CRIMES'] = (crime_filtered.iloc[:, 2:].sum(axis=1) / 2).astype(int)

# Drop columns
crime_filtered.drop(columns=['TOTAL IPC CRIMES'], inplace=True)

# List of columns to add to 'OTHER IPC CRIMES'
columns_to_add = [
    'ATTEMPT TO MURDER', 
    'CULPABLE HOMICIDE NOT AMOUNTING TO MURDER', 
    'PREPARATION AND ASSEMBLY FOR DACOITY',
    'CRIMINAL BREACH OF TRUST', 
    'COUNTERFIETING', 
    'ARSON', 
    'HURT/GREVIOUS HURT', 
    'DOWRY DEATHS', 
    'ASSAULT ON WOMEN WITH INTENT TO OUTRAGE HER MODESTY',
    'INSULT TO MODESTY OF WOMEN', 
    'CRUELTY BY HUSBAND OR HIS RELATIVES', 
    'IMPORTATION OF GIRLS FROM FOREIGN COUNTRIES',
    'CAUSING DEATH BY NEGLIGENCE'
]

# Add specified columns to 'OTHER IPC CRIMES'
crime_filtered['OTHER IPC CRIMES'] = crime_filtered[columns_to_add].sum(axis=1) + crime_filtered['OTHER IPC CRIMES']

# Drop the added columns
crime_filtered.drop(columns=columns_to_add, inplace=True)

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
    "DELHI UT": "dl",
    "PUDUCHERRY": "py"
}

# Define the list of duplicate districts
duplicate = ['NORTH', 'SOUTH', 'G.R.P.', 'CHANDIGARH', 'BALRAMPUR', 'BILASPUR',
             'EAST', 'WEST', 'GRP', 'CID', 'HAMIRPUR', 'RAILWAYS',
             'LAKSHADWEEP', 'PUDUCHERRY', 'PRATAPGARH']

# Define a function to update the district name
def update_district(row):
    # Check if the district is in the duplicate list
    if row['DISTRICT'] in duplicate:
        state_code = states_rto.get(row['STATE/UT'], "")
        # If a valid state code is found, append it to the district
        if state_code:
            return f"{row['DISTRICT']}_{state_code}"
    # Return the original district name if no change is needed
    return row['DISTRICT']

# Apply the function to the 'DISTRICT' column
crime_filtered['DISTRICT'] = crime_filtered.apply(update_district, axis=1)

# Assuming `crime_filtered` is your DataFrame
# Aggregate the data for the treemap
crime_filtered['STATE/UT'] = crime_filtered['STATE/UT'].astype(str)
crime_filtered['DISTRICT'] = crime_filtered['DISTRICT'].astype(str)

# Melting the dataframe to create a structure suitable for the treemap
crime_melted = crime_filtered.melt(id_vars=['STATE/UT', 'DISTRICT'], 
                                   value_vars=[col for col in crime_filtered.columns if col not in ['STATE/UT', 'DISTRICT', 'TOTAL CRIMES']])

# Create a sum for total IPC crimes at the root level
total_crimes = crime_filtered['TOTAL CRIMES'].sum()

# Now, build the necessary labels and parents for the treemap
labels = ['All Crimes']  # Root label
parents = ['']  # Root has no parent
values = [total_crimes]  # Root value

check = True

# Add the state/UTs as the next level
for state in crime_filtered['STATE/UT'].unique():
    state_crimes = crime_filtered[crime_filtered['STATE/UT'] == state]['TOTAL CRIMES'].sum()
    labels.append(state)
    parents.append('All Crimes')
    values.append(state_crimes)
    
    # Add districts under each state
    index = 0
    for district in crime_filtered[crime_filtered['STATE/UT'] == state]['DISTRICT'].unique():
        district_crimes = crime_filtered[crime_filtered['DISTRICT'] == district]['TOTAL CRIMES'].sum()
        if district in duplicate:
            labels.append(district + "_" + states_rto[state])
        else:
            labels.append(district)
        parents.append(state)
        values.append(district_crimes)
            
        # Add the types of crimes under each district
        for crime_type in crime_melted['variable'].unique():
            crime_value = crime_melted[(crime_melted['STATE/UT'] == state) & 
                                       (crime_melted['DISTRICT'] == district) & 
                                       (crime_melted['variable'] == crime_type)]['value'].sum()
            labels.append(crime_type + "_" + states_rto[state] + str(index))
            index = index + 1
            if district in duplicate:
                parents.append(district + "_" + states_rto[state])
            else:
                parents.append(district)
            # Fixing an inconsistency in dataset for one record
            if district == "VIRUDHUNAGAR" and check: 
                values.append(crime_value - 5)
                check = False
            else:
                values.append(crime_value)

# Convert values to Python native types (to handle numpy.int64)
values = [int(value) for value in values]

# Create the JSON object
treemap_data = {
    "labels": labels,
    "parents": parents,
    "values": values
}

# Write the JSON object to a JavaScript file
with open('../_TREEMAP_DATA/treemap_crime_rate.js', 'w') as f:
    f.write(f"const treemapData = {json.dumps(treemap_data)};")

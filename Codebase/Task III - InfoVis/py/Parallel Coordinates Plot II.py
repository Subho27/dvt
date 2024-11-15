import numpy as np
import pandas as pd
import json

crime_1 = pd.read_csv("../_DATASET/01_District_wise_crimes_committed_IPC_2001_2012.csv")
crime_2 = pd.read_csv("../_DATASET/01_District_wise_crimes_committed_IPC_2013.csv")

# Standardize column names for merging
crime_1_filtered = crime_1[['STATE/UT', 'YEAR', 'TOTAL IPC CRIMES']].groupby(['STATE/UT', 'YEAR']).sum().reset_index()
crime_2_filtered = crime_2[['STATE/UT', 'YEAR', 'TOTAL IPC CRIMES']].groupby(['STATE/UT', 'YEAR']).sum().reset_index()

# Combine all datasets into one
combined_crime = pd.concat([crime_1_filtered, crime_2_filtered])

# Sum up `TOTAL IPC CRIMES` across all data sources by `YEAR` and `STATE/UT`
combined_crime = combined_crime.groupby(['STATE/UT', 'YEAR']).sum().reset_index()

# Divide the `TOTAL IPC CRIMES` by 2
combined_crime['TOTAL IPC CRIMES'] = combined_crime['TOTAL IPC CRIMES'] // 2

combined_crime['STATE/UT'] = combined_crime['STATE/UT'].replace('A&N Islands', 'A & N ISLANDS')
combined_crime['STATE/UT'] = combined_crime['STATE/UT'].replace('D&N Haveli', 'D & N HAVELI')
combined_crime['STATE/UT'] = combined_crime['STATE/UT'].replace('Daman & Diu', 'DAMAN & DIU')
combined_crime['STATE/UT'] = combined_crime['STATE/UT'].str.upper()


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


# Replace the values in the 'STATE/UT' column using the dictionary
combined_crime['STATE/UT'] = combined_crime['STATE/UT'].replace(states_rto)


# Extract unique years as numbers and strings
years = sorted(combined_crime['YEAR'].unique())
years_str = [str(year) for year in years]

# Create a dictionary with each state/UT as a key
state_data = {}
for state in combined_crime['STATE/UT'].unique():
    state_crime_data = combined_crime[combined_crime['STATE/UT'] == state].sort_values('YEAR')['TOTAL IPC CRIMES'].tolist()
    # Ensure all elements are converted to Python int
    state_data[state] = [int(value) for value in state_crime_data]

# Combine into the final JSON object
crime_data_state = {
    "year": [int(year) for year in years], 
    "year_str": years_str,
    **state_data
}

# Convert to JavaScript syntax
data_js_content = f"const crime_data_state = {json.dumps(crime_data_state, indent=4)};"

# Save to a data.js file
with open("../_PCP_DATA/pcp_crime_rate_state.js", "w") as file:
    file.write(data_js_content)


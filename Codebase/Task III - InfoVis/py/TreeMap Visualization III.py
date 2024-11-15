import numpy as np
import pandas as pd
import json

crime = pd.read_csv("../_DATASET/23_Anti_corruprion_cases.csv")

# Selecting only specified columns
selected_columns = ['Area_Name', 'Year', 
                    'AC21_No_of_cases_withdrawn_or_other_wise_disposed_off_on_account_of_death_of_the_accused_during_the_year', 
                    'AC23_No_of_cases_convicted_during_the_year', 
                    'AC24_No_of_cases_acquitted_or_discharged_during_the_year', 
                    'AC25_No_of_cases_pending_trial_at_the_end_of_the_year']

crime = crime[selected_columns]

crime['Trials_Completed'] = (
    crime['AC23_No_of_cases_convicted_during_the_year'] +
    crime['AC24_No_of_cases_acquitted_or_discharged_during_the_year']
)

crime['Total_Cases_For_Trial'] = (
    crime['AC25_No_of_cases_pending_trial_at_the_end_of_the_year'] + crime['Trials_Completed'] +
    crime['AC21_No_of_cases_withdrawn_or_other_wise_disposed_off_on_account_of_death_of_the_accused_during_the_year']
)

# Renaming columns with a dictionary mapping old names to new names
renamed_columns = {
    'Area_Name': 'STATE/UT',
    'AC21_No_of_cases_withdrawn_or_other_wise_disposed_off_on_account_of_death_of_the_accused_during_the_year': 'Cases_Withdrawn_Death_Accused',
    'AC23_No_of_cases_convicted_during_the_year': 'Cases_Convicted',
    'AC24_No_of_cases_acquitted_or_discharged_during_the_year': 'Cases_Acquitted_Discharged',
    'AC25_No_of_cases_pending_trial_at_the_end_of_the_year': 'Pending_Trials_End_Year'
}

# Applying the renaming
crime = crime.rename(columns=renamed_columns)

states_rto = {
    "Arunachal Pradesh": "ar",
    "Andhra Pradesh": "ap",
    "Assam": "as",
    "Bihar": "br",
    "Chhattisgarh": "cg",
    "Gujarat": "gj",
    "Goa": "ga",
    "Himachal Pradesh": "hp",
    "Haryana": "hr",
    "Jharkhand": "jh",
    "Jammu & Kashmir": "jk",
    "Kerala": "kl",
    "Karnataka": "ka",
    "Maharashtra": "mh",
    "Manipur": "mn",
    "Madhya Pradesh": "mp",
    "Mizoram": "mz",
    "Meghalaya": "ml",
    "Nagaland": "nl",
    "Odisha": "od",
    "Punjab": "pb",
    "Rajasthan": "rj",
    "Sikkim": "sk",
    "Tamil Nadu": "tn",
    "Tripura": "tp",
    "Uttar Pradesh": "up",
    "Uttarakhand": "uk",
    "West Bengal": "wb",
    "Andaman & Nicobar Islands": "an",
    "Chandigarh": "ch",
    "Daman & Diu": "dd",
    "Dadra & Nagar Haveli": "dn",
    "Lakshadweep": "ld",
    "Delhi": "dl",
    "Puducherry": "py"
}

# Calculate the root sum
root_value = crime['Total_Cases_For_Trial'].sum()

# Initialize lists for the treemap
labels = ["Total Cases for Trial"]
parents = [""]
values =[root_value]

# Iterate over each year to add it as a child of the root
for year in crime['Year'].unique():
    # Sum Total_Cases_For_Trial for each year
    year_value = crime[crime['Year'] == year]['Total_Cases_For_Trial'].sum()
    labels.append(f"Year {year}")
    parents.append("Total Cases for Trial")
    values.append(year_value)
    
    # Iterate over each STATE/UT in the given year
    for state in crime[crime['Year'] == year]['STATE/UT'].unique():
        # Filter data for the specific year and state
        state_data = crime[(crime['Year'] == year) & (crime['STATE/UT'] == state)]
        state_value = state_data['Total_Cases_For_Trial'].values[0]
        
        labels.append(state + "_" + str(year)[-2:])
        parents.append(f"Year {year}")
        values.append(state_value)
        
        # Add children under the state level: Cases Withdrawn, Trials Completed, and Pending Trials
        labels.extend([
            f"Cases Withdrawn_{states_rto[state]}{str(year)[-2:]}", 
            f"Trials Completed_{states_rto[state]}{str(year)[-2:]}", 
            f"Pending Trials_{states_rto[state]}{str(year)[-2:]}"
        ])
        parents.extend([state + "_" + str(year)[-2:]] * 3)
        values.extend([
            state_data['Cases_Withdrawn_Death_Accused'].values[0],
            state_data['Trials_Completed'].values[0],
            state_data['Pending_Trials_End_Year'].values[0]
        ])
        
        # Add children under Trials Completed: Cases Convicted and Cases Acquitted/Discharged
        labels.extend([
            f"Cases Convicted_{states_rto[state]}{str(year)[-2:]}", 
            f"Cases Acquitted/Discharged_{states_rto[state]}{str(year)[-2:]}"
        ])
        parents.extend([f"Trials Completed_{states_rto[state]}{str(year)[-2:]}"] * 2)
        values.extend([
            state_data['Cases_Convicted'].values[0],
            state_data['Cases_Acquitted_Discharged'].values[0]
        ])

# Convert values to Python native types (to handle numpy.int64)
values = [int(value) for value in values]

# Create the JSON object
treemap_data = {
    "labels": labels,
    "parents": parents,
    "values": values
}

# Write the JSON object to a JavaScript file
with open('../_TREEMAP_DATA/treemap_crime_rate_anti_corruption.js', 'w') as f:
    f.write(f"const treemapData = {json.dumps(treemap_data)};")

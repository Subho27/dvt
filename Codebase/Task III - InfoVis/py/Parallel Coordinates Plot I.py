import numpy as np
import pandas as pd
import json


# Import data
ipc1 = pd.read_csv("../_DATASET/01_District_wise_crimes_committed_IPC_2001_2012.csv")
ipc2 = pd.read_csv("../_DATASET/01_District_wise_crimes_committed_IPC_2013.csv")
ipc3 = pd.read_csv("../_DATASET/01_District_wise_crimes_committed_IPC_2014.csv")

sc1 = pd.read_csv("../_DATASET/02_01_District_wise_crimes_committed_against_SC_2001_2012.csv")
sc2 = pd.read_csv("../_DATASET/02_01_District_wise_crimes_committed_against_SC_2013.csv")
sc3 = pd.read_csv("../_DATASET/02_01_District_wise_crimes_committed_against_SC_2014.csv")

st1 = pd.read_csv("../_DATASET/02_District_wise_crimes_committed_against_ST_2001_2012.csv")
st2 = pd.read_csv("../_DATASET/02_District_wise_crimes_committed_against_ST_2013.csv")
st3 = pd.read_csv("../_DATASET/02_District_wise_crimes_committed_against_ST_2014.csv")

woman1 = pd.read_csv("../_DATASET/42_District_wise_crimes_committed_against_women_2001_2012.csv")
woman2 = pd.read_csv("../_DATASET/42_District_wise_crimes_committed_against_women_2013.csv")
woman3 = pd.read_csv("../_DATASET/42_District_wise_crimes_committed_against_women_2014.csv")

child1 = pd.read_csv("../_DATASET/03_District_wise_crimes_committed_against_children_2001_2012.csv")
child2 = pd.read_csv("../_DATASET/03_District_wise_crimes_committed_against_children_2013.csv")


# Data Preprocessing - total ipc crimes
ipc1_yearwise = ipc1[['YEAR', 'TOTAL IPC CRIMES']].groupby('YEAR').sum().reset_index()
ipc2_yearwise = ipc2[['YEAR', 'TOTAL IPC CRIMES']].groupby('YEAR').sum().reset_index()
ipc3_yearwise = ipc3[['Year', 'Total Cognizable IPC crimes']].groupby('Year').sum().reset_index()

ipc1_yearwise['TOTAL IPC CRIMES'] = (ipc1_yearwise['TOTAL IPC CRIMES'] / 2).astype(int)
ipc2_yearwise['TOTAL IPC CRIMES'] = (ipc2_yearwise['TOTAL IPC CRIMES'] / 2).astype(int)
ipc3_yearwise['Total Cognizable IPC crimes'] = (ipc3_yearwise['Total Cognizable IPC crimes'] / 2).astype(int)

ipc3_yearwise.rename(columns={
    'Year': 'YEAR',
    'Total Cognizable IPC crimes': 'TOTAL IPC CRIMES'
}, inplace=True)

ipc = pd.concat([ipc1_yearwise, ipc2_yearwise, ipc3_yearwise], ignore_index=True)


# Data Preprocessing - total ipc crimes against SC
sc1['TOTAL IPC CRIMES against SC'] = sc1.iloc[:, 3:].sum(axis=1)
sc2['TOTAL IPC CRIMES against SC'] = sc2.iloc[:, 3:].sum(axis=1)

sc1_yearwise = sc1[['Year', 'TOTAL IPC CRIMES against SC']].groupby('Year').sum().reset_index()
sc2_yearwise = sc2[['Year', 'TOTAL IPC CRIMES against SC']].groupby('Year').sum().reset_index()
sc3_yearwise = sc3[['Year', 'Total crimes against SCs']].groupby('Year').sum().reset_index()

sc1_yearwise['TOTAL IPC CRIMES against SC'] = (sc1_yearwise['TOTAL IPC CRIMES against SC'] / 2).astype(int)
sc2_yearwise['TOTAL IPC CRIMES against SC'] = (sc2_yearwise['TOTAL IPC CRIMES against SC'] / 2).astype(int)
sc3_yearwise['Total crimes against SCs'] = (sc3_yearwise['Total crimes against SCs'] / 2).astype(int)

sc1_yearwise.rename(columns={'Year': 'YEAR'}, inplace=True)
sc2_yearwise.rename(columns={'Year': 'YEAR'}, inplace=True)
sc3_yearwise.rename(columns={
    'Year': 'YEAR',
    'Total crimes against SCs': 'TOTAL IPC CRIMES against SC'
}, inplace=True)

sc = pd.concat([sc1_yearwise, sc2_yearwise, sc3_yearwise], ignore_index=True)


# Data Preprocessing - total ipc crimes against ST
st1['TOTAL IPC CRIMES against ST'] = st1.iloc[:, 3:].sum(axis=1)
st2['TOTAL IPC CRIMES against ST'] = st2.iloc[:, 3:].sum(axis=1)

st1_yearwise = st1[['Year', 'TOTAL IPC CRIMES against ST']].groupby('Year').sum().reset_index()
st2_yearwise = st2[['Year', 'TOTAL IPC CRIMES against ST']].groupby('Year').sum().reset_index()
st3_yearwise = st3[['Year', 'Total crimes against STs']].groupby('Year').sum().reset_index()

st1_yearwise['TOTAL IPC CRIMES against ST'] = (st1_yearwise['TOTAL IPC CRIMES against ST'] / 2).astype(int)
st2_yearwise['TOTAL IPC CRIMES against ST'] = (st2_yearwise['TOTAL IPC CRIMES against ST'] / 2).astype(int)
st3_yearwise['Total crimes against STs'] = (st3_yearwise['Total crimes against STs'] / 2).astype(int)

st1_yearwise.rename(columns={'Year': 'YEAR'}, inplace=True)
st2_yearwise.rename(columns={'Year': 'YEAR'}, inplace=True)
st3_yearwise.rename(columns={
    'Year': 'YEAR',
    'Total crimes against STs': 'TOTAL IPC CRIMES against ST'
}, inplace=True)

st = pd.concat([st1_yearwise, st2_yearwise, st3_yearwise], ignore_index=True)


# Data Preprocessing - total ipc crimes against WOMEN
woman1['TOTAL IPC CRIMES against WOMEN'] = woman1.iloc[:, 3:].sum(axis=1)
woman2['TOTAL IPC CRIMES against WOMEN'] = woman2.iloc[:, 3:].sum(axis=1)

woman1_yearwise = woman1[['Year', 'TOTAL IPC CRIMES against WOMEN']].groupby('Year').sum().reset_index()
woman2_yearwise = woman2[['Year', 'TOTAL IPC CRIMES against WOMEN']].groupby('Year').sum().reset_index()
woman3_yearwise = woman3[['Year', 'Total Crimes against Women']].groupby('Year').sum().reset_index()

woman1_yearwise['TOTAL IPC CRIMES against WOMEN'] = (woman1_yearwise['TOTAL IPC CRIMES against WOMEN'] / 2).astype(int)
woman2_yearwise['TOTAL IPC CRIMES against WOMEN'] = (woman2_yearwise['TOTAL IPC CRIMES against WOMEN'] / 2).astype(int)
woman3_yearwise['Total Crimes against Women'] = (woman3_yearwise['Total Crimes against Women'] / 2).astype(int)

woman1_yearwise.rename(columns={'Year': 'YEAR'}, inplace=True)
woman2_yearwise.rename(columns={'Year': 'YEAR'}, inplace=True)
woman3_yearwise.rename(columns={
    'Year': 'YEAR',
    'Total Crimes against Women': 'TOTAL IPC CRIMES against WOMEN'
}, inplace=True)

woman = pd.concat([woman1_yearwise, woman2_yearwise, woman3_yearwise], ignore_index=True)


# Data Preprocessing - total ipc crimes against CHILDREN
child1_yearwise = child1[['Year', 'Total']].groupby('Year').sum().reset_index()
child2_yearwise = child2[['Year', 'Total']].groupby('Year').sum().reset_index()

child1_yearwise['Total'] = (child1_yearwise['Total'] / 2).astype(int)
child2_yearwise['Total'] = (child2_yearwise['Total'] / 2).astype(int)

child1_yearwise.rename(columns={'Total': 'TOTAL IPC CRIMES against CHILDREN'}, inplace=True)
child2_yearwise.rename(columns={'Total': 'TOTAL IPC CRIMES against CHILDREN'}, inplace=True)

child = pd.concat([child1_yearwise, child2_yearwise], ignore_index=True)


# Preparing data for PCP 
# Remove the last row from each DataFrame
# As 2014 data not available for children
ipc = ipc.iloc[:-1]
sc = sc.iloc[:-1]
st = st.iloc[:-1]
woman = woman.iloc[:-1]

# Combine the data into a single dictionary
data = {
    'year': ipc['YEAR'].tolist(),
    'year_str': ipc['YEAR'].astype(str).tolist(),
    'ipc': ipc['TOTAL IPC CRIMES'].tolist(),
    'sc': sc['TOTAL IPC CRIMES against SC'].tolist(),
    'st': st['TOTAL IPC CRIMES against ST'].tolist(),
    'woman': woman['TOTAL IPC CRIMES against WOMEN'].tolist(),
    'child': child['TOTAL IPC CRIMES against CHILDREN'].tolist(),
}

# Convert data to JSON format for JavaScript
js_data = f"""
const crime_data = {{
    year: {data['year']},
    year_str: {data['year_str']},
    ipc: {data['ipc']},
    sc: {data['sc']},
    st: {data['st']},
    woman: {data['woman']},
    child: {data['child']}
}};
"""

# Write the JavaScript file
with open('../_PCP_DATA/pcp_crime_rate.js', 'w') as js_file:
    js_file.write(js_data)
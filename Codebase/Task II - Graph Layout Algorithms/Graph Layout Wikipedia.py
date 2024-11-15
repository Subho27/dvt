import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import re
import imageio

import warnings
warnings.filterwarnings('ignore')

# Load the data from the text file
with open('./_DATASET/wiki-RfA.txt', 'r', encoding="utf-8") as file:
    data = file.read().strip()

# Split entries by double newline
entries = data.split('\n\n')

# Define lists to store data for each column
src, tgt, vot, res, yea, dat, txt = [], [], [], [], [], [], []

# Parse each entry
for entry in entries:
    # Use regular expressions to find each field's value
    src.append(re.search(r'SRC:(.*)', entry).group(1).strip())
    tgt.append(re.search(r'TGT:(.*)', entry).group(1).strip())
    vot.append(int(re.search(r'VOT:(.*)', entry).group(1).strip()))
    res.append(int(re.search(r'RES:(.*)', entry).group(1).strip()))
    yea.append(int(re.search(r'YEA:(.*)', entry).group(1).strip()))
    dat.append(re.search(r'DAT:(.*)', entry).group(1).strip())
    txt.append(re.search(r'TXT:(.*)', entry).group(1).strip())

# Create a DataFrame
df = pd.DataFrame({
    'SRC': src,
    'TGT': tgt,
    'VOT': vot,
    'RES': res,
    'YEA': yea,
    'DAT': dat,
    'TXT': txt
})

# Split entries by double newline
entries = data.split('\n\n')

# Initialize dictionary to store DataFrames for each year
yearly_edge_dfs = {}

# Loop through each year from 2003 to 2013
for year in range(2003, 2014):
    # Initialize lists to store edge information for the specific year
    src_list = []
    tgt_list = []
    weight_list = []
    res_list = []

    # Extract SRC, TGT, VOT, YEA, and RES values from each entry
    for entry in entries:
        src_match = re.search(r'SRC:(.*)', entry)
        tgt_match = re.search(r'TGT:(.*)', entry)
        vot_match = re.search(r'VOT:(.*)', entry)
        yea_match = re.search(r'YEA:(.*)', entry)
        res_match = re.search(r'RES:(.*)', entry)

        # Append values if the year matches the current year in the loop
        if (src_match and tgt_match and vot_match and yea_match and res_match and
            yea_match.group(1).strip() == str(year)):
            src_list.append(src_match.group(1).strip())
            tgt_list.append(tgt_match.group(1).strip())
            weight_list.append(int(vot_match.group(1).strip()))
            res_list.append(int(res_match.group(1).strip()))

    # Create an Edge DataFrame for the specific year
    edge_df_year = pd.DataFrame({
        'Source': src_list,
        'Target': tgt_list,
        'Type': 'directed',           # Set 'type' as 'directed' for all edges
        'id': range(len(src_list)),    # Generate unique id for each edge
        'weight': weight_list,         # Use 'VOT' values as 'weight'
        'RES': res_list                # Add 'RES' values as a new column
    })
    
    # Store the DataFrame in the dictionary with the year as the key
    yearly_edge_dfs[year] = edge_df_year

    # Optionally, dynamically assign the DataFrame to a variable
    globals()[f'edge_df_{year}'] = edge_df_year

# Dictionary to store edge DataFrames for each year, assuming you have already created them
# Replace `yearly_edge_dfs` with your actual dictionary or list of yearly edge DataFrames
yearly_edge_dfs = {2003: edge_df_2003, 2004: edge_df_2004, 2005: edge_df_2005, 2006: edge_df_2006, 
                   2007: edge_df_2007, 2008: edge_df_2008, 2009: edge_df_2009, 2010: edge_df_2010, 
                   2011: edge_df_2011, 2012: edge_df_2012, 2013: edge_df_2013}

# Loop through each year and apply cleaning steps to each edge_df_YEAR
for year, edge_df in yearly_edge_dfs.items():
    # Ensure 'Source' and 'Target' columns are strings
    edge_df['Source'] = edge_df['Source'].astype(str)
    edge_df['Target'] = edge_df['Target'].astype(str)
    
    # Convert 'weight' column to numeric, setting invalid weights to NaN
    edge_df['weight'] = pd.to_numeric(edge_df['weight'], errors='coerce')
    
    # Replace NaN values in 'weight' with a default value (e.g., 1)
    edge_df['weight'].fillna(1, inplace=True)
    
    # Remove rows with any NaN in 'Source', 'Target', or 'weight'
    edge_df.dropna(subset=['Source', 'Target', 'weight'], inplace=True)
    
    # Reset index after dropping rows to avoid gaps
    edge_df = edge_df.reset_index(drop=True)
    
    # Assign a unique ID to each edge
    edge_df['id'] = edge_df.index
    
    # Set 'Type' column to 'directed' for all edges
    edge_df['Type'] = 'directed'
    
    # Store back the cleaned DataFrame in the dictionary (optional, for clarity)
    yearly_edge_dfs[year] = edge_df

# Initialize an empty DataFrame to store the top 10 nodes for each year
top_nodes_df = pd.DataFrame(columns=['Year', 'Node ID', 'In-Degree', 'Key Incoming Sources', 'Observations'])

# Define a function to extract the top 10 nodes by in-degree
def get_top_10_nodes_by_indegree(graph, year):
    # Calculate in-degree for each node and sort by descending order
    in_degrees = sorted(graph.in_degree(), key=lambda x: x[1], reverse=True)
    
    # Get top 10 nodes by in-degree
    top_10_nodes = in_degrees[:10]
    
    # Collect data for the table
    data = []
    for node, indegree in top_10_nodes:
        # Get incoming sources for each top node
        incoming_sources = [source for source, target in graph.in_edges(node)]
        
        # Construct observations if needed (for example, describe significant influence)
        observation = f"Node {node} has significant influence from {len(incoming_sources)} sources."
        
        # Append data to list
        data.append([year, node, indegree, ', '.join(incoming_sources[:5]), observation])  # limit incoming sources display to 5
    
    return pd.DataFrame(data, columns=['Year', 'Node ID', 'In-Degree', 'Key Incoming Sources', 'Observations'])

# Loop through each year's edge DataFrame to populate the table
for year, edge_df in yearly_edge_dfs.items():
    # Create a directed graph from the edge DataFrame for each year
    G = nx.from_pandas_edgelist(edge_df, source='Source', target='Target', edge_attr='weight', create_using=nx.DiGraph())
    
    # Get top 10 nodes by in-degree for the current year and append to the main DataFrame
    year_df = get_top_10_nodes_by_indegree(G, year)
    top_nodes_df = pd.concat([top_nodes_df, year_df], ignore_index=True)

# Reset index of the final DataFrame
top_nodes_df.reset_index(drop=True, inplace=True)

top_nodes_df.to_csv('./output/top_10_nodes_summary.csv', index=False)

yearly_edge_dfs = {2003: edge_df_2003, 2004: edge_df_2004, 2005: edge_df_2005, 2006: edge_df_2006, 
                   2007: edge_df_2007, 2008: edge_df_2008, 2009: edge_df_2009, 2010: edge_df_2010, 
                   2011: edge_df_2011, 2012: edge_df_2012, 2013: edge_df_2013}

# Loop through each year and create and save the graph as GEXF
for year, edge_df in yearly_edge_dfs.items():
    # Step 1: Create a directed graph using NetworkX
    G = nx.from_pandas_edgelist(edge_df, source='Source', target='Target', edge_attr='weight', create_using=nx.DiGraph())

    # Step 2: Add nodes (if not already added)
    # Each node ID is unique, and we don't need to add extra attributes for now
    for node in G.nodes():
        G.nodes[node]['id'] = node  # Ensuring the node ID exists as an attribute

    # Step 3: Write the graph to a GEXF file
    output_path = f"./output/graph_{year}.gexf"
    nx.write_gexf(G, output_path)

# Dictionary of edge DataFrames for each year, assuming these are created earlier
yearly_edge_dfs = {2003: edge_df_2003, 2004: edge_df_2004, 2005: edge_df_2005, 2006: edge_df_2006, 
                   2007: edge_df_2007, 2008: edge_df_2008, 2009: edge_df_2009, 2010: edge_df_2010, 
                   2011: edge_df_2011, 2012: edge_df_2012, 2013: edge_df_2013}

for year, edge_df in yearly_edge_dfs.items():
    # Step 1: Create a directed graph using NetworkX
    G = nx.from_pandas_edgelist(edge_df, source='Source', target='Target', edge_attr='weight', create_using=nx.DiGraph())
    
    # Step 2: Calculate the in-degree of each node and select the top 10 nodes
    top_10_nodes = sorted(G.in_degree(), key=lambda x: x[1], reverse=True)[:10]
    top_10_node_ids = [node[0] for node in top_10_nodes]
    
    # Step 3: Identify all source nodes that connect to the top 10 nodes
    # Initialize a set with the top 10 nodes
    nodes_to_include = set(top_10_node_ids)
    
    # For each top node, add its predecessors (source nodes with edges to it)
    for target_node in top_10_node_ids:
        predecessors = G.predecessors(target_node)
        nodes_to_include.update(predecessors)
    
    # Step 4: Create a subgraph containing the top 10 nodes and all source nodes
    subgraph = G.subgraph(nodes_to_include).copy()  # Copy to ensure it’s a separate graph
    
    # Step 5: Add node attributes to ensure Gephi compatibility (optional)
    for node in subgraph.nodes():
        subgraph.nodes[node]['id'] = node  # Ensure the node ID exists as an attribute
    
    # Step 6: Write the subgraph to a GEXF file
    output_path = f"./output/top_10_with_sources_graph_{year}.gexf"
    nx.write_gexf(subgraph, output_path)

# Step 1: Split entries by double newline
entries = data.split('\n\n')

# Initialize lists to store the data
src_list = []
tgt_list = []
vot_list = []
yea_list = []
res_list = []

# Extract SRC, TGT, VOT, YEA, and RES values from each entry
for entry in entries:
    src_match = re.search(r'SRC:(.*)', entry)
    tgt_match = re.search(r'TGT:(.*)', entry)
    vot_match = re.search(r'VOT:(.*)', entry)
    yea_match = re.search(r'YEA:(.*)', entry)
    res_match = re.search(r'RES:(.*)', entry)  # Match RES values

    # Append values if the year is 2008 or greater
    if src_match and tgt_match and vot_match and yea_match and res_match:
        year = int(yea_match.group(1).strip())  # Ensure year is numeric
        if year >= 2008:
            src_list.append(src_match.group(1).strip())
            tgt_list.append(tgt_match.group(1).strip())
            vot_list.append(int(vot_match.group(1).strip()))
            yea_list.append(int(yea_match.group(1).strip()))  # Assuming 'YEA' is a numeric value
            res_list.append(int(res_match.group(1).strip()))  # Assuming 'RES' is a numeric value

# Step 2: Create a DataFrame with the filtered data
edge_df = pd.DataFrame({
    'Source': src_list,
    'Target': tgt_list,
    'Type': 'directed',          
    'id': range(len(src_list))
})

# Clean the edge Data
# Ensure that 'Source' and 'Target' are valid and numeric, 'Weight' is numeric
edge_df['Source'] = edge_df['Source'].astype(str)  # Ensure source is string
edge_df['Target'] = edge_df['Target'].astype(str)  # Ensure target is string

# Assign an ID to each edge
edge_df['id'] = edge_df.index

# Ensure that 'Type' column is set to 'directed' for all edge
edge_df['Type'] = 'directed'

# Clean the edge Data: Remove rows with any empty or NaN cells in 'Source', 'Target', or 'Weight'
edge_df.dropna(subset=['Source', 'Target'], inplace=True)  # Ensure no missing values in critical columns

# Reset index after dropping rows to avoid gaps in the index
edge_df = edge_df.reset_index(drop=True)

G = nx.from_pandas_edgelist(edge_df, source='Source', target='Target', create_using=nx.DiGraph())

output_path = "./output/graph_export.gexf"
nx.write_gexf(G, output_path)

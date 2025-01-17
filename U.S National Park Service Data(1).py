#!/usr/bin/env python
# coding: utf-8

# In[16]:


import pandas as pd
import plotly.graph_objects as go


# In[17]:


file_path = r"C:\Users\timot\Downloads\Combined_recreation_visit_data.csv"
data = pd.read_csv(file_path)


# In[18]:


print(data.columns)


# In[19]:


data.columns = data.columns.str.strip()
print(data.columns)


# In[20]:


data['Value'] = data['Value'].str.strip()  # Remove any leading/trailing spaces
data['Value'] = pd.to_numeric(data['Value'], errors='coerce')  # Convert to numeric


# In[24]:


# Create a unique list of all nodes
nodes = list(set(data['Source'].tolist() + data['Target'].tolist()))
node_indexes = {name: i for i, name in enumerate(nodes)}

# Map source and target indexes for reversed flow
data['Reversed_Source'] = data['Target']
data['Reversed_Target'] = data['Source']

source_indexes = [node_indexes[source] for source in data['Reversed_Source']]
target_indexes = [node_indexes[target] for target in data['Reversed_Target']]

# Add total visit numbers to node labels
node_labels = [
    f"{node}: {int(data[data['Source'] == node]['Value'].sum())}" if node in data['Source'].values 
    else f"{node}" for node in nodes
]

# Defining colors for states and regions
state_colors = {
    state: f"rgba({(index * 60) % 255}, {(index * 90) % 255}, {(index * 120) % 255}, 0.8)"
    for index, state in enumerate(data['Target'].unique())
}
region_color = "rgba(0, 204, 102, 0.8)"  # Uniform green for all regions → total visits

# colors assigned based on flow
link_colors = [
    state_colors[target] if target in state_colors else region_color
    for source, target in zip(data['Reversed_Source'], data['Reversed_Target'])
]

# Create the Sankey diagram
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=20, 
        thickness=20,
        line=dict(color="black", width=0.5),
        label=node_labels,
        color="rgba(0, 0, 0, 0.6)",
    ),
    link=dict(
        source=[node_indexes[src] for src in data['Reversed_Source']],
        target=[node_indexes[tgt] for tgt in data['Reversed_Target']],
        value=data['Value'],
        color=link_colors,
    )
)])

# Layout customization
fig.update_layout(
    title_text= "U.S. National Park Visit Data (1979-2023)",
    font=dict(size=12, family="Arial"),
    height=800, 
    width=1000,
    paper_bgcolor="white",
    plot_bgcolor="white",
)

fig.write_html("US_National_Park_Visit_sankey_diagram.html")

# Display the updated diagram
fig.show()


# In[ ]:





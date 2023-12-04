import pandas as pd
import plotly.express as px
import numpy as np

# Load your data
df = pd.read_csv('chicagolibrary.csv')  # Replace with your actual file path
print(df.columns)

# Exclude the rows which contain longitude, latitude data, and renovation years
df = df.iloc[:-3, :]

# Filter out the data for the years 2020 and 2023
df = df[~df['Year'].isin([2020, 2023])]

# Ensure the months are in the correct order
months_order = [
    "JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE",
    "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"
]

# Convert the 'BRANCH' column to a categorical type with ordered categories
df['BRANCH'] = pd.Categorical(df['BRANCH'], categories=months_order, ordered=True)

# Sort the dataframe by 'BRANCH' to ensure the months are in chronological order
df.sort_values('BRANCH', inplace=True)

# Melt the dataframe to a long format suitable for a heat map
df_melted = df.melt(id_vars='BRANCH', var_name='Branch', value_name='Visitors')

# Add a small constant to avoid taking the log of zero
df_melted['Visitors_Log'] = np.log(df_melted['Visitors'] + 1)

# Create the heat map using a logarithmic color scale
fig = px.density_heatmap(
    df_melted,
    x='Branch',
    y='BRANCH',
    z='Visitors_Log',
    category_orders={"BRANCH": months_order},
    title='Heat Map of Monthly Visitors by Branch in Chicago Libraries (Excluding 2020 and 2023)',
    color_continuous_scale='YlGnBu'  # This is a perceptually uniform color scale
)

# Improve the hover text by mapping the logarithmic values back to the original visitor counts
fig.update_traces(
    hovertemplate=df_melted.apply(lambda row: f'Branch: {row["Branch"]}<br>Month: {row["BRANCH"]}<br>Visitors: {int(np.exp(row["Visitors_Log"]) - 1)}', axis=1)
)

# Show the figure
fig.show()

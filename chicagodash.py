from dash import Dash, dcc, html, Input, Output
import dash
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np

# Load your data
cl = pd.read_csv('chicagolibrary.csv')

# Create a list of branch names
clkeys= list(cl.keys())[1:82]

# Store the sums of the given year (2022)
cl2022 = cl[cl['Year'] == 2022]
cl2022
cl2022.loc['Total'] = cl2022.sum()
result = [x/1000 for x in list(cl2022.loc['Total', :])[1:82]]

# Create a figure and store the longitude and latitude values
fig = go.Figure()

lon = list()
lat = list()

for i in range(len(clkeys)):
    lon.append(cl.loc[58][clkeys[i]])
    lat.append(cl.loc[59][clkeys[i]])


# Show the figure
fig.add_trace(go.Scattermapbox(
        lon = lon,
        lat = lat,
        marker = dict(size = result,
                      sizemode = 'area',
                      color = 'Red'),
        text = [clkeys[i] + '<br>' + 'Total Visitor Count was ' + str(int(result[i] * 1000)) + ' in 2022' for i in range(len(clkeys))],
        name = ""))

fig.update_layout(
        title_text = '2022 Chicago Visitors',
        showlegend = False,
        geo = dict(
            scope = 'usa',
            landcolor = 'rgb(217, 217, 217)'
        ),
    mapbox_style="open-street-map",
    mapbox_layers=[
        {
            "below": 'traces',
            "sourcetype": "raster",
            "sourceattribution": "United States Geological Survey",
            "source": [
                "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
            ]
        }
      ]
    )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                  autosize=True,
                 mapbox = dict(
                     center=dict(
                        lat=41.83017199,
                        lon=-87.67359301
                    ),
                    pitch=0,
                    zoom=9
                 ))
fig.update_geos(fitbounds="locations")


##### VIZ 2 #########

# Load your data
df = pd.read_csv('chicagolibrary.csv')  # Replace with your actual file path

# Exclude the last two rows which contain longitude and latitude data
df = df.iloc[:-2, :-1]  # Also exclude the 'Year' column

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
fig2 = px.density_heatmap(
    df_melted,
    x='Branch',
    y='BRANCH',
    z='Visitors_Log',
    category_orders={"BRANCH": months_order},
    title='Heat Map of Monthly Visitors by Branch in Chicago Libraries',
    labels={'BRANCH': 'Month'},
    color_continuous_scale='YlGnBu'  # This is a perceptually uniform color scale
)

fig2.update_layout(height=600)

# Improve the hover text by mapping the logarithmic values back to the original visitor counts
fig2.update_traces(
    hovertemplate=df_melted.apply(lambda row: f'Branch: {row["Branch"]}<br>Month: {row["BRANCH"]}<br>Visitors: {int(row["Visitors"])}', axis=1)
)


############## VIZ 3 ################

# Load your data
df = pd.read_csv('chicagolibrary_2.csv')  # Replace with your actual file path

# Assume the last row contains the renovation years
renovation_years = df.iloc[-1, 1:-1]
renovation_years.fillna(1900, inplace=True)  # Replace NaN with 1900

# Create a DataFrame for the renovation years
df_renovation_years = pd.DataFrame({
    'Branch': renovation_years.index,
    'Renovation Year': renovation_years.values
})

# In the app layout definition
interactive_html = html.Div([
    # Input for the cutoff year
    dcc.Input(id='input-year', type='number', value=pd.to_datetime('today').year - 10,
              min=1980, max=pd.to_datetime('today').year, step=1),
    html.Button('Submit', id='submit-val', n_clicks=0),
    html.Br(),
    # Div to hold the graph with the corrected config for double-click
    dcc.Graph(
        id='renovation-bar-chart',
        config={'doubleClick': 'reset'},
        responsive='auto' # This will reset the axes to the initial state defined in the figure's layout
    )
])

def app_callback(app):
    @app.callback(
        Output('renovation-bar-chart', 'figure'),
        [Input('submit-val', 'n_clicks')],
        [dash.dependencies.State('input-year', 'value')])
    def update_graph(n_clicks, input_value):
        # Filter the data based on the input year
        df_renovation_years['Recently Renovated'] = df_renovation_years['Renovation Year'] >= input_value
        df_filtered = df_renovation_years.sort_values(by='Renovation Year', ascending=True)

        # Create the updated figure
        fig = px.bar(
            df_filtered,
            x='Renovation Year',
            y='Branch',
            color='Recently Renovated',
            orientation='h',
            title=f'Renovation Year of Chicago Library Branches (Cutoff: {input_value})'
        )

        # Adjust the x-axis range to start at 1980
        fig.update_xaxes(
            title='Renovation Year',
            range=[1980, pd.to_datetime('today').year + 1],  # Set the range from 1980 to current year
            autorange=False
        )

        # Adjust the layout for the figure height and y-axis labels
        fig.update_layout(
            height=1200,  # Increase the figure height to accommodate more y-axis labels
            yaxis_title='Branch',
            coloraxis_colorbar=dict(
                title='Renovated After Cutoff?',
                tickvals=[False, True],
                ticktext=['No', 'Yes']
            )
        )

        # Update y-axis configuration for better label visibility
        fig.update_yaxes(
            automargin=True,  # Automatically adjust the margin size to prevent cut-off
            tickangle=0,  # Keep the labels horizontal for better readability
            tickfont=dict(size=10)  # Adjust the font size if necessary
        )

        return fig


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Monthly Heatmap', children=[
            dcc.Graph(
                figure=fig2
            )
        ]),
        dcc.Tab(label='Renovation Year', children=interactive_html),
        dcc.Tab(label='Geographic Rendering', children=[
            dcc.Graph(
                figure=fig
            )
        ]),
    ])
])

app_callback(app)

if __name__ == '__main__':
    app.run(debug=True)

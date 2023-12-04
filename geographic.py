import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Load your data
cl = pd.read_csv('chicagolibrary.csv')

# Create a list of branch names
clkeys= list(cl.keys())[1:82]

# Store the sums of the given year (2022)
cl2022 = cl[cl['Year'] == 2022]
cl2022
cl2022.loc['Total'] = cl2022.sum()
result = [x/2000 for x in list(cl2022.loc['Total', :])[1:82]]

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
        text = clkeys,
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

fig.show()
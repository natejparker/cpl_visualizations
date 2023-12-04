import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

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

# Initialize the Dash app
app = dash.Dash(__name__)

# In the app layout definition
app.layout = html.Div([
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


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)


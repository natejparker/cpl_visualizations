import pandas as pd
import plotly.express as px

chicago_df = pd.read_csv('chicagolibrary.csv')

monthly_visitors = chicago_df.iloc[:-2, 1:-1].sum(axis=1)
plot_data = pd.DataFrame({
    'Month': chicago_df['BRANCH'][:-2],
    'Total Visitors': monthly_visitors,
    'Year': chicago_df['Year'][:-2]
})

average_visitors_per_month = plot_data.groupby('Month')['Total Visitors'].mean().reset_index()

# Create the initial line plot
fig = px.line(plot_data, x='Month', y='Total Visitors', color='Year',
              title='Total Number of Visitors by Month in Chicago Libraries',
              labels={'Total Visitors': 'Number of Visitors'},
              category_orders={'Month': ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"]})

# Add the average line
fig.add_scatter(x=average_visitors_per_month['Month'], y=average_visitors_per_month['Total Visitors'],
                mode='lines', name='Average', line=dict(color='black', dash='dash'))

# Show the plot
fig.show()

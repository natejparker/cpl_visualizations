import pandas as pd
import plotly.express as px

chicago_df = pd.read_csv('chicagolibrary.csv')

monthly_visitors = chicago_df.iloc[:-2, 1:-1].sum(axis=1)
plot_data = pd.DataFrame({
    'Month': chicago_df['BRANCH'][:-2],
    'Total Visitors': monthly_visitors,
    'Year': chicago_df['Year'][:-2]
})

fig = px.line(plot_data, x='Month', y='Total Visitors', color='Year',
              title='Total Number of Visitors by Month in Chicago Libraries',
              labels={'Total Visitors': 'Number of Visitors'},
              category_orders={'Month': ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"]})

fig.show()

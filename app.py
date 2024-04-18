import pandas as pd                 # needed to read in data into dataframes and manipulate
import plotly.express as px         # needed to create line graph
from dash import Dash, dcc, html, Input, Output, callback    # needed to create ui components

df = pd.read_csv('data/clean_data.csv')
# drop the first column
df = df.drop(df.columns[0], axis=1)

min_year = df['Year'].min()
max_year = df['Year'].max()

stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]  # load the CSS stylesheet

app = Dash(__name__, external_stylesheets=stylesheets)  # initialize the app
server = app.server

app.layout = html.Div(
    [
        html.H1("Emissions Data Across Countries over Time"),  # app title at top of page
        html.Div(
            children=[
                html.Div(
                    dcc.Dropdown(df["Country"], id="country-dropdown", placeholder="Select countries", multi=True),     # use dataframe's countries values in dropdown, also set placeholder and allow multi select
                    className="six columns",    # take up half the width, next to range slider
                ),
                html.Div(
                    dcc.RangeSlider(id="year-slider", min=min_year, max=max_year, step=1, value=[min_year, max_year], marks={str(i): str(i) for i in range(min_year, max_year + 1, 20)}),   # create range slider with min and max years defined earlier, set default value, and set marks every 20 years
                    className="six columns",    # take up half the width, next to dropdown
                ),
            ],
            className="row",    # together make dropdown and range slider take up fill width of page in a single row
        ),
        dcc.Graph(id='result-graph'),  # setup graph component with fig defined earlier
    ],
    className="row",    # take up fill width of page and layout into seperate rows
)

@callback(
    Output('result-graph', 'figure'),
    Input('country-dropdown', 'value'),
    Input('year-slider', 'value'))
def update_graph(selected_countries, selected_year_range):
    # filter for selected year range, selected_year_range is [min_year, max_year]
    filtered_df = df[(df['Year'] >= selected_year_range[0]) & (df['Year'] <= selected_year_range[1])]
    
    # if countries are selected, filter for those
    if selected_countries is not None and len(selected_countries) > 0:
        filtered_df = filtered_df[filtered_df['Country'].isin(selected_countries)]  # .isin checks if value is in array

    # create line graph with x axis as the year from df, y as the gdpPercap from df, and group by country into different colors, also set title and axis labels
    fig = px.line(filtered_df, x="Year", y="CO2 Emissions (kt)", color="Country", title="Carbon Dioxide Emissions Over Time by Country")

    return fig

if __name__ == "__main__":
    app.run_server(debug=True)      # run the app
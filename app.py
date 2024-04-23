import pandas as pd                 # needed to read in data into dataframes and manipulate
import plotly.express as px         
from dash import Dash, dcc, html, Input, Output, callback    # needed to create ui components

df = pd.read_csv('data/clean_data.csv')
# drop the first column
df = df.drop(df.columns[0], axis=1)

min_year = df['Year'].min()
max_year = df['Year'].max()

df['Country'] = df['Country'].replace({
    'United Kingdom of Great Britain and Northern Ireland': 'U.K.',
    'United States of America': 'U.S.',
    'Russian Federation': 'Russia'
})

countries = df["Country"].unique()
countries_with_all_data = []

for country in countries:
    missing = False
    for year in range(1990, 2019):
        # get row for country and year
        row = df[(df["Country"] == country) & (df["Year"] == year)]
        # loop over all columns for that row
        for col in row.columns:
            if row.empty or pd.isna(row[col].values[0]):
                missing = True
                break
    if not missing:
        countries_with_all_data.append(country)

stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]  # load the CSS stylesheet

app = Dash(__name__, external_stylesheets=stylesheets)  # initialize the app
server = app.server

app.layout = html.Div(
    [
        html.Div(
            [
                html.H1(
                    "🌎 Environmentalist Dashboard",
                    style={
                        "textAlign": "center",
                        "margin-bottom": "2vw",
                        "margin-top": "2vw",
                    },
                ),  # app title at top of page
                html.Div(
                    children=[
                        html.Div(
                            dcc.Dropdown(
                                value="Racing Bar Chart",
                                options=[
                                    "Racing Bar Chart",
                                    "Stacked Area Chart",
                                    "Line Graph",
                                ],
                                id="graph-dropdown",
                                placeholder="Select Graph",
                                clearable=False,
                            ),  # use dataframe's countries values in dropdown, also set placeholder and allow multi select
                            className="four columns",  # take up half the width, next to range slider
                        ),
                        html.Div(
                            dcc.Dropdown(
                                df["Country"],
                                value=[
                                    "France",
                                    "U.K.",
                                    "Spain",
                                    "Italy",
                                    "Australia",
                                    "Romania",
                                    "Ukraine",
                                ],
                                id="country-dropdown",
                                placeholder="Select Countries",
                                multi=True,
                            ),  # use dataframe's countries values in dropdown, also set placeholder and allow multi select
                            className="four columns",  # take up half the width, next to range slider
                        ),
                        html.Div(
                            dcc.Dropdown(
                                df.columns[2 : len(df.columns) - 1],
                                id="emissions-dropdown",
                                placeholder="Select Emmitted Gas",
                                multi=True,
                            ),  # use dataframe's countries values in dropdown, also set placeholder and allow multi select
                            className="four columns",  # take up half the width, next to range slider
                        ),
                    ],
                    style={
                        "margin-bottom": "3vw",
                        "margin-left": "3vw",
                        "margin-right": "3vw",
                    },
                    className="row",  # together make dropdowns take up fill width of page in a single row
                ),
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                dcc.Graph(
                                    id="result-graph"
                                ),  # setup graph component with fig defined earlier
                                html.Div(
                                    id="slider-container",
                                    children=[
                                        dcc.RangeSlider(
                                            id="year-slider",
                                            min=min_year,
                                            max=max_year,
                                            step=1,
                                            value=[min_year, max_year],
                                            marks={
                                                str(i): str(i)
                                                for i in range(
                                                    min_year, max_year + 1, 2
                                                )
                                            },
                                        )
                                    ],  # create range slider with min and max years defined earlier, set default value, and set marks every 20 years
                                    # className="six columns",  # take up half the width, next to dropdown
                                ),
                            ],
                            className="eight columns",
                        ),
                        html.Div(
                            children=[
                                html.Div(
                                    children=[
                                        html.H4("Important legislation"),
                                        html.P(
                                            "1. Kyoto Protocol (1997) - This treaty set country-specific targets for reducing greenhouse gas emissions, marking a significant international commitment to combat global warming."
                                        ),
                                        html.P(
                                            "2. European Union Emission Trading Scheme (EU ETS) (2005) - The EU's cap-and-trade system incentivized companies to reduce emissions by allowing them to buy or sell emission allowances."
                                        ),
                                        html.P(
                                            "3. Paris Agreement (2015) - This agreement aimed to limit global warming to well below 2°C by requiring increasing commitments from all participating countries."
                                        ),
                                    ]
                                )
                            ],
                            className="four columns",
                        ),
                    ],
                    # make this div use display flex and align items to center
                    style={
                        "display": "flex",
                        "align-items": "center",
                        "margin-left": "2vw",
                        "margin-right": "2vw",
                        "height": "60%",
                    },
                ),
            ],
            style={"height": "95vh"},
            className="row",  # take up fill width of page and layout into seperate rows
        ),
        html.Div(
            [
                html.H1("About"),
                html.H3("Who this dashboard is for"),
                html.P(
                    "I built this dashboard to serve the persona of a global environmentalist, who will want to visualize the progress that has been made towards reducing climate change over the years, with a special interest in the progress across countries. An accurate measure of this progress can be obtained by visualizing the amount of emissions of different chemicals. \
            This dashboard lets them compare different countries down to the emission of specific chemicals like greenhouse gasses, toxic gasses, etc. over time (since 1990) to overall get a better understanding of the global climate. It also provides desciptions of a few of the most important environmental legislations that have been passed in the past few decades. The dashboard can help show their affect on the \
                emissions of various countries."
                ),
                html.H3("Data Provenance"),
                html.P(
                    'I retrieved the downloaded files from a kaggle dataset: https://www.kaggle.com/datasets/ruchi798/global-environmental-indicators. The reason this data was collected is "Environmental indicators help us to understand and analyze the health of the planet. Indicators are simple measures that provide an effective and economical way to track the state of the environment and may warn us of impending environmental problems. These in turn can help enhance policy makers\' and regulators\' ability to manage and resolve these problems before it’s too late. Let’s do our bit to save the environment and take responsibility to take care of it." I agree with this statement and used a subset of the csv files (the files for emissions of different chemicals under the "Air and Climate" folder) for my interactive dashboard.'
                ),
                html.Br(),
                html.P(
                    'In terms of where the data for the kaggle dataset comes from, the author says "Statistics on Water and Waste are based on official statistics supplied by national statistical offices and/or ministries of environment (or equivalent institutions) in response to the biennial UNSD/UNEP Questionnaire on Environment Statistics, complemented with comparable statistics from OECD and Eurostat, and water resources data from FAO Aquastat. Statistics on other themes were compiled by UNSD from other international sources. In a few cases, UNSD has made some calculations in order to derive the indicators. However, generally no adjustments have been made to the values received from the source.'
                ),
                html.Br(),
                html.P("The URL of the source is https://unstats.un.org/home/"),
            ],
            style={"text-align": "center", "margin-bottom": "2vw", "margin-top": "1vw", "margin-left": "2vw", "margin-right": "2vw"},
        ),
    ]
)


@app.callback(Output("country-dropdown", "options"), Input("graph-dropdown", "value"))
def update_dropdown(graph_type):
    if graph_type == "Racing Bar Chart":
        return countries_with_all_data
    else:
        return df["Country"]


@app.callback(
    Output("emissions-dropdown", "multi"),
    Input("graph-dropdown", "value"),
)
def update_emissions_dropdown(graph_type):
    if (
        graph_type == "Line Graph"
        or graph_type == "Stacked Area Chart"
        or "Racing Bar Chart"
    ):
        return False
    else:
        return True


@app.callback(
    Output("year-slider", "min"),
    Output("year-slider", "max"),
    Output("year-slider", "value"),
    Output("year-slider", "marks"),
    Input("country-dropdown", "value"),
)
def update_slider(selected_countries):
    if selected_countries is not None and len(selected_countries) > 0:
        filtered_df = df[df["Country"].isin(selected_countries)]
        min_year = filtered_df["Year"].min()
        max_year = filtered_df["Year"].max()
    else:
        min_year = df["Year"].min()
        max_year = df["Year"].max()

    marks = {str(i): str(i) for i in range(min_year, max_year + 1, 2)}
    value = [min_year, max_year]

    return min_year, max_year, value, marks


@app.callback(
    Output("result-graph", "figure"),
    Input("year-slider", "value"),
    Input("country-dropdown", "value"),
    Input("graph-dropdown", "value"),
    Input("emissions-dropdown", "value"),
)
def update_graph(selected_years, selected_countries, graph_type, selected_emissions):
    if graph_type == "Line Graph":
        if selected_countries is None or selected_countries == []:
            filtered_df = df[df["Year"].between(selected_years[0], selected_years[1])]
        else:
            filtered_df = df[
                (df["Year"].between(selected_years[0], selected_years[1]))
                & (df["Country"].isin(selected_countries))
            ]

        if (
            selected_emissions is None
            or selected_emissions == []
            or (isinstance(selected_emissions, list) and len(selected_emissions) > 1)
        ):
            y_value = "Total Emissions (kt)"
        else:
            y_value = (
                selected_emissions
                if isinstance(selected_emissions, str)
                else selected_emissions[0]
            )

        fig = px.line(
            filtered_df,
            x="Year",
            y=y_value,
            color="Country",
            title="Global Greenhouse Gas Emissions by Country over Time",
        )
        fig.update_layout(showlegend=False)
        fig.update_layout(
            xaxis=dict(
                showline=True,
                linewidth=1,
                linecolor="#566573",
                gridcolor="#566573",  # make grid lines transparent
            ),
            yaxis=dict(
                showline=True,
                linewidth=1,
                linecolor="#566573",
                gridcolor="#566573",  # make grid lines transparent
            ),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )
    elif graph_type == "Stacked Area Chart":
        if selected_countries is None or selected_countries == []:
            filtered_df = df[df["Year"].between(selected_years[0], selected_years[1])]
        else:
            filtered_df = df[
                (df["Year"].between(selected_years[0], selected_years[1]))
                & (df["Country"].isin(selected_countries))
            ]

        # drop rows where country is china or india
        # filtered_df = filtered_df[~filtered_df["Country"].isin(["China", "India"])]

        if (
            selected_emissions is None
            or selected_emissions == []
            or (isinstance(selected_emissions, list) and len(selected_emissions) > 1)
        ):
            y_value = "Total Emissions (kt)"
        else:
            y_value = (
                selected_emissions
                if isinstance(selected_emissions, str)
                else selected_emissions[0]
            )

        fig = px.area(
            filtered_df,
            x="Year",
            y=y_value,
            color="Country",
            title="Global Greenhouse Gas Emissions by Country over Time",
        )
        fig.update_layout(showlegend=False)
        fig.update_layout(
            xaxis=dict(
                showline=True,
                linewidth=1,
                linecolor="#566573",
                gridcolor="#566573",  # make grid lines transparent
            ),
            yaxis=dict(
                showline=True,
                linewidth=1,
                linecolor="#566573",
                gridcolor="#566573",  # make grid lines transparent
            ),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )
    elif graph_type == "Racing Bar Chart":
        if selected_countries is None or selected_countries == []:
            filtered_df = df[
                (df["Year"].between(selected_years[0], selected_years[1]))
                & (df["Country"].isin(countries_with_all_data))
            ]
        else:
            filtered_df = df[
                (df["Year"].between(selected_years[0], selected_years[1]))
                & (df["Country"].isin(selected_countries))
            ]

        if (
            selected_emissions is None
            or selected_emissions == []
            or (isinstance(selected_emissions, list) and len(selected_emissions) > 1)
        ):
            y_value = "Total Emissions (kt)"
        else:
            y_value = (
                selected_emissions
                if isinstance(selected_emissions, str)
                else selected_emissions[0]
            )

        fig = px.bar(
            filtered_df,
            x=y_value,
            y="Country",
            animation_frame="Year",
            orientation="h",
            range_x=[0, filtered_df[y_value].max()],
            title="Global Greenhouse Gas Emissions by Country over Time",
        )

        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        fig.update_layout(
            xaxis=dict(
                showline=True,
                linewidth=1,
                linecolor="#566573",
                gridcolor="#566573",  # make grid lines transparent
            ),
            yaxis=dict(
                showline=True,
                linewidth=1,
                linecolor="#566573",
                gridcolor="#566573",  # make grid lines transparent
            ),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)      # run the app
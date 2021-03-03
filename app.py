import os
import pathlib
import numpy as np
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
import dash_daq as daq
from dash.dependencies import Input, Output, State

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    external_stylesheets=[dbc.themes.SLATE],  # Darkly?
)
server = app.server
app.title = "Predictive Maintenance Dashboard"


def Header(name, app):
    title = html.H1(name)
    logo = html.Img(
        src=app.get_asset_url("dash-logo.png"), style={"float": "right", "height": 30}
    )
    link = html.A(logo, href="https://plotly.com/dash/")
    return dbc.Row([dbc.Col(title, md=8), dbc.Col(link, md=4)], align="center")


active_power_display = dbc.Card(
    className="mt-auto",
    children=[
        dbc.CardBody(
            [
                html.Div(
                    daq.Gauge(
                        id="active-power-information-gauge",
                        label="Active Power",
                        min=0,
                        max=20000,  # This one should be the theoretical maximum
                        value=100,
                        units="MW",  # Check the correct units
                        showCurrentValue=True,
                    ),
                    className="m-auto",
                )
            ],
            className="d-flex",
        ),
    ],
)

reactive_power_display = dbc.Card(
    className="mt-auto",
    children=[
        dbc.CardBody(
            [
                daq.Gauge(
                    id="reactive-power-information-gauge",
                    label="Reactive Power",
                    min=0,
                    max=10000,  # This one should be the theoretical maximum
                    value=20,  # float(temp_val)
                    units="MVAR",  # Check the correct units
                    showCurrentValue=True,
                ),
            ],
            className="d-flex",
        ),
    ],
)

df = pd.read_csv("data/SCADA_data.csv")
df = df.set_index("Time")


app.layout = dbc.Container(
    [
        Header("Predictive Maintenance for Wind Farms Dashboard", app),
        html.Hr(),
        dbc.Row(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(
                                    id="Main-Graph",
                                ),
                            ],
                            style={"width": "98%", "display": "inline-block"},
                        ),
                        html.Div(
                            [
                                dcc.Dropdown(
                                    id="dropdown",
                                    options=[
                                        {"label": label, "value": label}
                                        for label in df.columns
                                    ],
                                    value="",
                                    multi=False,
                                    searchable=False,
                                )
                            ],
                            style={"width": "33%", "display": "inline-block"},
                        ),
                    ]
                )
            ]
        ),
        html.Hr(),
        dbc.Row([active_power_display, reactive_power_display]),

    ]
)


@app.callback(Output("Main-Graph", "figure"), [Input("dropdown", "value")])
def update_graph(selected_column):
    if selected_column in list(df):
        return go.Figure(data=[go.Scatter(x=df.index, y=df[selected_column])])
    else:
        return {}


if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=True)

import os
import pathlib
import numpy as np
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from datetime import datetime, date
import dash_daq as daq
from dash.dependencies import Input, Output, State

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    external_stylesheets=[dbc.themes.SLATE],  # Darkly?
)
server = app.server
app.title = "Predictive Maintenance Dashboard"

# Load data
df = pd.read_csv("data/SCADA_data.csv")
df['Time'] = pd.to_datetime(df['Time'], dayfirst=True, errors='coerce')
first_date = df['Time'].iloc[0]
last_date = df['Time'].iloc[-1]


# df = df.set_index("Time")
# first_date = df.index[0]
# last_date = df.index[-1]


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

graphs = dbc.Card(
    className="mt-auto",
    children=[
        dbc.CardBody(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(
                                    id="Main-Graph", config={"displayModeBar": False}
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
        )
    ],
)

date_selector = dbc.Card(
    className="mt-auto",
    children=[
        html.Div(
            [
                dcc.DatePickerRange(
                    id="date-picker",
                    min_date_allowed=date(2014, 5, 1),
                    max_date_allowed=date(2015, 4, 9),
                    initial_visible_month=date(2014, 5, 1),
                    start_date_placeholder_text="Start Period",
                    end_date_placeholder_text="End Period",
                    calendar_orientation="vertical"
                ),
                html.Div(id="output-container-date-picker-range"),
            ]
        )
    ],
)

app.layout = dbc.Container(
    [
        Header("Predictive Maintenance for Wind Farms Dashboard", app),
        html.Hr(),
        graphs,
        html.Hr(),
        dbc.Row([date_selector]),
        html.Hr(),
        dbc.Row([active_power_display, reactive_power_display]),
    ]
)


@app.callback(Output("Main-Graph", "figure"),
              [Input("dropdown", "value"),
               Input('date-picker', 'start_date'),
               Input('date-picker', 'end_date')])
def update_graph(selected_column, start_date, end_date):
    if selected_column in list(df):
        if start_date and end_date:
            start_date_object = datetime.strptime(start_date, '%Y-%m-%d')
            end_date_object = datetime.strptime(end_date, '%Y-%m-%d')
            mask = (df['Time'] > start_date_object) & (df['Time'] <= end_date_object)
            df_within_dates = df.loc[mask]
            fig = go.Figure(data=[go.Scatter(x=df_within_dates['Time'],
                                             y=df_within_dates[selected_column])])
            fig.update_layout(
                xaxis=dict(
                    showline=True,
                    showgrid=False,
                    showticklabels=True,
                    linecolor='rgb(204, 204, 204)',
                    linewidth=2,
                    ticks='outside',
                    tickfont=dict(
                        family='Arial',
                        size=12,
                        color='rgb(82, 82, 82)',
                    ),
                ),
                yaxis=dict(
                    showgrid=False,
                    zeroline=False,
                    showline=False,
                    showticklabels=False,
                ),
                autosize=False,
                margin=dict(
                    autoexpand=False,
                    l=100,
                    r=20,
                    t=110,
                ),
                showlegend=False,
                plot_bgcolor='white'
            )
            return fig
        elif start_date:
            start_date_object = datetime.strptime(start_date, '%Y-%m-%d')
            mask = (df['Time'] > start_date_object)
            df_within_dates = df.loc[mask]
            fig = go.Figure(data=[go.Scatter(x=df_within_dates['Time'],
                                             y=df_within_dates[selected_column])])
            fig.update_layout(
                xaxis=dict(
                    showline=True,
                    showgrid=False,
                    showticklabels=True,
                    linecolor='rgb(204, 204, 204)',
                    linewidth=2,
                    ticks='outside',
                    tickfont=dict(
                        family='Arial',
                        size=12,
                        color='rgb(82, 82, 82)',
                    ),
                ),
                yaxis=dict(
                    showgrid=False,
                    zeroline=False,
                    showline=False,
                    showticklabels=False,
                ),
                autosize=False,
                margin=dict(
                    autoexpand=False,
                    l=100,
                    r=20,
                    t=110,
                ),
                showlegend=False,
                plot_bgcolor='white'
            )
            return fig
        else:
            fig = go.Figure(data=[go.Scatter(x=df['Time'], y=df[selected_column])])
            fig.update_layout(
                xaxis=dict(
                    showline=True,
                    showgrid=False,
                    showticklabels=True,
                    linecolor='rgb(204, 204, 204)',
                    linewidth=2,
                    ticks='outside',
                    tickfont=dict(
                        family='Arial',
                        size=12,
                        color='rgb(82, 82, 82)',
                    ),
                ),
                yaxis=dict(
                    showgrid=False,
                    zeroline=False,
                    showline=False,
                    showticklabels=False,
                ),
                autosize=False,
                margin=dict(
                    autoexpand=False,
                    l=100,
                    r=20,
                    t=110,
                ),
                showlegend=False,
                plot_bgcolor='white'
            )
            return fig
    else:
        return {}


if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=True)

"""
References:
https://stackoverflow.com/questions/66027814/plotly-dash-embed-indicator-graph-inside-of-a-dbc-card
https://plotlydash.com/pie-chart-with-drop-down-list-and-date-picker-range-in-plotly-dash/
"""

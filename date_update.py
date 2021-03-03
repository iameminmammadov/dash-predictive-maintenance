import os
import pathlib
import numpy as np
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from datetime import date, datetime
import plotly.graph_objs as go
import plotly.express as px
import dash_daq as daq
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__,
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
                external_stylesheets=[dbc.themes.SLATE]  # Darkly?
                )
server = app.server
app.title = "Predictive Maintenance Dashboard"

df = pd.read_csv('data/SCADA_data.csv')
df = df.set_index('Time')

first_date = df.index[0]
last_date = df.index[-1]

app.layout = html.Div([
    dcc.DatePickerRange(
        id='date-picker',
        min_date_allowed=first_date,
        max_date_allowed=last_date,
        start_date_placeholder_text="Start Period",
        end_date_placeholder_text="End Period",
        calendar_orientation="vertical"
        # initial_visible_month=date(2014, 5, 1),
        # end_date=date(2014, 5, 31)
    ),
    html.Div(id='output-container-date-picker-range')
])

@app.callback(
    dash.dependencies.Output('output-container-date-picker-range', 'children'),
    [dash.dependencies.Input('date-picker', 'start_date'),
     dash.dependencies.Input('date-picker', 'end_date')])
def update_output(start_date, end_date):
    string_prefix = "You have selected: "
    if start_date is not None:
        # start_date_object = date.fromisoformat(start_date)
        # start_date_string = start_date_object.strftime('%B %d, %Y')
        start_date_object = datetime.strptime(first_date, '%d/%m/%Y %H:%M:%S')
        start_date_string = start_date_object.strftime("%B %d, %Y - %H:%M:%S")
        string_prefix = string_prefix + "Start Date: " + start_date_string
    if end_date is not None:
        end_date_object = datetime.strptime(first_date, '%d/%m/%Y %H:%M:%S')
        end_date_string = end_date_object.strftime("%B %d, %Y - %H:%M:%S")
        string_prefix = string_prefix + 'End Date: ' + end_date_string
    if len(string_prefix) == len("You have selected: "):
        return "Select a date to display"
    else:
        return string_prefix

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)

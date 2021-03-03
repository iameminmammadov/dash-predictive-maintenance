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

"""
References:
https://www.kaggle.com/wasuratme96/turbine-fault-prediction
"""

df = pd.read_csv("data/SCADA_data.csv")
df = df.set_index("Time")

app.layout = html.Div(
    [
        dcc.Textarea(id="Main-TextArea", persistence=True, persistence_type="local"),
        html.Div(
            [
                dcc.Dropdown(
                    id="dropdown",
                    options=[{"label": label, "value": label} for label in df.columns],
                    value="",
                    multi=False,
                    searchable=False,
                )
            ],
            style={"width": "33%", "display": "inline-block"},
        ),
    ]
)

column_description = {
    "WEC: ava. windspeed": "Average Windspeed",
    "WEC : max. windspeed": "Maximum Windspeed",
    "WEC: ava. Rotation": "Average rotation",
}


@app.callback(Output("Main-TextArea", "value"), [Input("dropdown", "value")])
def update_text(selected_column):
    if selected_column in list(df):
        return "You chose the following column: \n{}".format(selected_column)
    else:
        return "Nothing to display so far"


if __name__ == "__main__":
    app.run_server(debug=True)

"""
 'WEC: ava. windspeed',
 'WEC : max. windspeed',
 'WEC : min. windspeed',
 'WEC: ava. Rotation',
 'WEC: max. Rotation',
 'WEC: min. Rotation',
 'WEC: ava. Power',
 'WEC: max. Power',
 'WEC: min. Power',
 'WEC: ava. Nacel position including cable twisting',
 'WEC: Operating Hours',
 'WEC: Production kWh',
 'WEC: Production minutes',
 'WEC: ava. reactive Power',
 'WEC: max. reactive Power',
 'WEC: min. reactive Power',
 'WEC: ava. available P from wind',
 'WEC: ava. available P technical reasons',
 'WEC: ava. Available P force majeure reasons',
 'WEC: ava. Available P force external reasons',
 'WEC: ava. blade angle A',
 'CS101 : Sys 1 inverter 1 cabinet temp.',
 'CS101 : Sys 1 inverter 2 cabinet temp.',
 'CS101 : Sys 1 inverter 3 cabinet temp.',
 'CS101 : Sys 1 inverter 4 cabinet temp.',
 'CS101 : Sys 1 inverter 5 cabinet temp.',
 'CS101 : Sys 1 inverter 6 cabinet temp.',
 'CS101 : Sys 1 inverter 7 cabinet temp.',
 'CS101 : Sys 2 inverter 1 cabinet temp.',
 'CS101 : Sys 2 inverter 2 cabinet temp.',
 'CS101 : Sys 2 inverter 3 cabinet temp.',
 'CS101 : Sys 2 inverter 4 cabinet temp.',
 'CS101 : Sys 2 inverter 5 cabinet temp.',
 'CS101 : Sys 2 inverter 6 cabinet temp.',
 'CS101 : Sys 2 inverter 7 cabinet temp.',
 'CS101 : Spinner temp.',
 'CS101 : Front bearing temp.',
 'CS101 : Rear bearing temp.',
 'CS101 : Pitch cabinet blade A temp.',
 'CS101 : Pitch cabinet blade B temp.',
 'CS101 : Pitch cabinet blade C temp.',
 'CS101 : Blade A temp.',
 'CS101 : Blade B temp.',
 'CS101 : Blade C temp.',
 'CS101 : Rotor temp. 1',
 'CS101 : Rotor temp. 2',
 'CS101 : Stator temp. 1',
 'CS101 : Stator temp. 2',
 'CS101 : Nacelle ambient temp. 1',
 'CS101 : Nacelle ambient temp. 2',
 'CS101 : Nacelle temp.',
 'CS101 : Nacelle cabinet temp.',
 'CS101 : Main carrier temp.',
 'CS101 : Rectifier cabinet temp.',
 'CS101 : Yaw inverter cabinet temp.',
 'CS101 : Fan inverter cabinet temp.',
 'CS101 : Ambient temp.',
 'CS101 : Tower temp.',
 'CS101 : Control cabinet temp.',
 'CS101 : Transformer temp.',
 'RTU: ava. Setpoint 1']
"""

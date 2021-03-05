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

app.layout = html.Div([
    dbc.Button("Predict", id='predict-button', outline=True,
               color='Primary', size="lg", className="mr-1")
    # html.Span
])


@app.callback(Output("predict-button", "children"),
              [Input("predict-button", "n_clicks")])
def action_on_predict(n):
    if n is None:
        return "Not Clicked"
    else:
        return "Predict button works"


if __name__ == "__main__":
    app.run_server(debug=True)

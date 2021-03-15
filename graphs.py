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

df = pd.read_csv("data/SCADA_data.csv")
df = df.set_index("Time")

# app.layout = html.Div([
#     html.Div([
#             dcc.Graph(
#                 id='Main-Graph',
#                 figure={'layout': go.Layout()}
#             ),
#         ], style={'width': '98%', 'display': 'inline-block'}
#     ),
#     html.Div([
#         dcc.Dropdown(
#             id='dropdown',
#             options=[{'label': label, 'value': label} for label in df.columns],
#             value='',
#             multi=False,
#             searchable=False)],
#         style={'width': '33%', 'display': 'inline-block'})
# ]
# )
fig = go.Figure()
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
                                    id="Main-Graph",
                                    config={"displayModeBar": False},
                                    figure=fig
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

app.layout = dbc.Container(
    [
        graphs,
        html.Hr(),
    ]
)


@app.callback(Output("Main-Graph", "figure"), [Input("dropdown", "value")])
def update_graph(selected_column):
    if selected_column in list(df):
        fig = go.Figure(data=[go.Scatter(x=df.index, y=df[selected_column])])
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


# app.layout = html.Div([
#     dcc.Textarea(
#         id='textarea-state-example',
#         style={'width': '98%', 'display': 'inline-block'}
#     ),
#     html.Div([
#         dcc.Dropdown(
#             id='dropdown',
#             options=[{'label': label, 'value': label} for label in df.columns],
#             value='',
#             multi=False,
#             searchable=False)],
#         style={'width': '33%', 'display': 'inline-block'})
# ]
# )
#
# @app.callback(
#     Output('textarea-state-example-output', 'children'),
#     Input('textarea-state-example-button', 'n_clicks'),
#     State('textarea-state-example', 'value')
# )
# def update_output(n_clicks, value):
#     if n_clicks > 0:
#         return 'You have entered: \n{}'.format(value)
#
# if __name__ == '__main__':
#     app.run_server(debug=True)

import pandas as pd
import numpy as np
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq

import plotly.graph_objs as go
from dash.dependencies import Input, Output
from datetime import datetime, date

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    external_stylesheets=[dbc.themes.SUPERHERO],  # SLATE
)
server = app.server
app.title = "Predictive Maintenance Dashboard"


def logo(app):
    title = html.H5(
        "PREDICTIVE MAINTENANCE DASHBOARD FOR WIND TURBINES", style={"margin-top": 5}
    )
    info_about_app = html.H6(
        "This Dashboard is focused on estimating the Remaining Useful Life (RUL) in wind turbines. RUL is defined "
        " as the time until the next fault."
    )
    logo_image = html.Img(
        src=app.get_asset_url("dash-logo.png"), style={"float": "right", "height": 50}
    )
    link = html.A(logo_image, href="https://plotly.com/dash/")

    return dbc.Row(
        [dbc.Col([dbc.Row([title]), dbc.Row([info_about_app])]), dbc.Col(link)]
    )


df = pd.read_csv("data/scada_data.csv")
df['Time'] = pd.to_datetime(df['Time'], dayfirst=True, errors='coerce')  # May, 1 until March, 12
df.sort_values(by="Time", axis=0, inplace=True)
df.reset_index(drop=True, inplace=True)

first_date = df["Time"].iloc[0]
last_date = df["Time"].iloc[0]

predict_button = dbc.Card(
    className="mt-auto",
    children=[
        dbc.CardBody(
            [
                html.Div(
                    [
                        dbc.Button(
                            "Predict",
                            id="predict-button",
                            outline=True,
                            color="Primary",
                            size="md",
                        ),
                    ]
                )
            ],
            style={"text-align": "center"},
        )
    ],
)

get_new_information_button = dbc.Card(
    className="mt-auto",
    children=[
        dbc.CardBody(
            [
                html.Div(
                    [
                        dbc.Button(
                            "Get New Data",
                            id="get-new-info-button",
                            outline=True,
                            color="Primary",
                            size="md",
                            className="mr-1",
                        )
                    ]
                )
            ],
            style={"text-align": "center"},
        )
    ],
)

graphs = dbc.Card(
    children=[
        dbc.CardBody(
            [
                html.Div(
                    [
                        dcc.Graph(
                            id="Main-Graph",
                            figure={
                                "layout": {
                                    "margin": {"t": 30, "r": 35, "b": 40, "l": 50},
                                    "xaxis": {
                                        "dtick": 5,
                                        "gridcolor": "#636363",
                                        "showline": False,
                                    },
                                    "yaxis": {"showgrid": False, "showline": False},
                                    "plot_bgcolor": "#2b2b2b",
                                    "paper_bgcolor": "#2b2b2b",
                                    "font": {"color": "gray"},
                                },
                            },
                            config={"displayModeBar": False},
                        ),
                        html.Pre(id='update-on-click-data'),
                    ],
                    style={"width": "98%", "display": "inline-block"},
                ),
                html.Div(
                    [
                        dcc.Dropdown(
                            id="feature-dropdown",
                            options=[
                                {"label": label, "value": label} for label in df.columns
                            ],
                            value="",
                            multi=False,
                            searchable=False,
                        )
                    ],
                    style={
                        "width": "33%",
                        "display": "inline-block",
                        "color": "black",
                    },
                ),
                html.Div(
                    [
                        dcc.DatePickerRange(
                            id="date-picker",
                            min_date_allowed=date(2014, 5, 1),  # need to change this
                            max_date_allowed=date(2015, 4, 9),
                            initial_visible_month=date(2014, 5, 1),
                            start_date_placeholder_text="Start Period",
                            end_date_placeholder_text="End Period",
                            calendar_orientation="vertical",
                        ),
                        html.Div(id="output-container-date-picker-range"),
                    ],
                    style={
                        "vertical-align": "top",
                        "position": "absolute",
                        "right": "3%",
                        "float": "right",
                        "display": "inline-block",
                    },
                ),
            ],
        )
    ]
)

rul_estimation_indicator = dbc.Card(
    children=[
        dbc.CardHeader("System RUL Estimation (days)",
                       style={"text-align": "center"}, ),
        dbc.CardBody(
            [
                daq.LEDDisplay(
                    id='rul_estimation_indicator"',
                    size=24,
                    color="#fec036",
                    style={"color": "#black"},
                    backgroundColor="#2b2b2b",
                    value="1234.56",
                )
            ],
            style={"text-align": "center"},
        ),
    ]
)

"""
message = dbc.FormGroup([dbc.Label("Message", html_for="example-message-row", width=2)
                    ,dbc.Col(dbc.Textarea(id = "example-message-row"
                                        , className="mb-3"
                                        , placeholder="Enter message"
                                        , required = True)
                            , width=10)
                ], row=True)
"""

info_box = dbc.Card(
    className="mt_auto",
    children=[
        dbc.CardBody(
            [
                html.Div(
                    dcc.Textarea(
                        id="Info-Textbox",
                        # className="mb-3",
                        placeholder="This field is used to display information about a feature displayed "
                                    "on the graph and estimated RUL. In order to estimate the RUL, use "
                                    "the button 'Get New Data' and then, 'Predict'. The estimated RUL will be "
                                    "printed.",
                        rows=10,
                        style={
                            "width": "100%",
                            "height": "100%",
                            "background-color": "#20304C",
                            "color": "red",
                            "placeholder": "red",
                            "fontFamily": "Arial",
                            "fontSize": "16",
                            "display": "inline-block",
                        },
                    )
                )
            ]
        )
    ],
)

# https://stackoverflow.com/questions/57433300/how-to-adjust-the-margins-in-plotly-dash-daq-components
# daq.Gauge(
#         color={'ranges':{'red':[0,2.5],'green':[2.5,10]}},
#         value=2,
#         label={'label':'FUEL', 'style':{'font-size':'30px'}},
#         max=10,
#         min=0,
#         scale={'custom':{'0':{'label':'E', 'style':{'font-size':'30px'}},
#                          '5':{'label':'1/2', 'style':{'font-size':'30px'}},
#                          '10':{'label':'F', 'style':{'font-size':'30px'}},
#                         }
#               }
#     ),

active_power_display = dbc.Card(
    children=[
        dbc.CardHeader("Active Power [kW]",
                       style={"text-align": "center"}),
        dbc.CardBody(
            [
                html.Div(
                    daq.Gauge(
                        id="active-power-information-gauge",
                        min=min(df['WEC: ava. Power']),
                        max=max(df['WEC: ava. Power']),  # This one should be the theoretical maximum
                        value=100,
                        showCurrentValue=True,
                        color="#fec036",
                        style={
                            "marginTop": "5%",
                            "marginBottom": "-10%",
                        },
                    ),
                    style={
                        "backgroundColor": "black",
                        "border-radius": "1px",
                        "border-width": "5px",
                        "border-top": "1px solid rgb(216, 216, 216)",
                    },
                )
            ],
        ),
    ],
)

active_power_from_wind_display = dbc.Card(
    children=[
        dbc.CardHeader("Active Power Available\n from Wind [kW]",
                       style={"text-align": "center",
                              "display": "flex"}),
        dbc.CardBody(
            [
                html.Div(
                    daq.Gauge(
                        id="active-power-from-wind-information-gauge",
                        min=min(df['WEC: ava. available P from wind']),
                        max=max(df['WEC: ava. available P from wind']),
                        value=10,
                        showCurrentValue=True,
                        color="#fec036",
                        style={
                            "display": "flex",
                            "marginTop": "5%",
                            "marginBottom": "-10%",
                        },
                    ),
                    className="m-auto",
                    style={
                        "display": "flex",
                        "backgroundColor": "black",
                        "border-radius": "1px",
                        "border-width": "5px",
                        "border-top": "1px solid rgb(216, 216, 216)",
                    },
                )
            ], className="d-flex",

        ),
    ],
)

wind_speed_information = dbc.Card(
    className="mt-auto",
    children=[
        dbc.CardHeader("Wind Speed [m/s]",
                       style={"text-align": "center"}),
        dbc.CardBody(
            [
                html.Div(
                    daq.Gauge(
                        id="wind-power-information-gauge",
                        min=min(df['WEC: ava. windspeed']),
                        max=int(max(df['WEC: ava. windspeed'])),
                        value=0,
                        showCurrentValue=True,
                        color="#fec036",
                        style={
                            "marginTop": "5%",
                            "marginBottom": "-10%",
                        },
                    ),
                    style={
                        "backgroundColor": "black",
                        "border-radius": "1px",
                        "border-width": "5px",
                        "border-top": "1px solid rgb(216, 216, 216)",
                    },
                )
            ],
        ),
    ],
)

reactive_power_display = dbc.Card(
    className="mt-auto",
    children=[
        dbc.CardHeader("Reactive Power [kVAR]",
                       style={"text-align": "center"}),
        dbc.CardBody(
            [
                html.Div(
                    daq.Gauge(
                        id="reactive-power-information-gauge",
                        min=min(df['WEC: ava. reactive Power']),
                        max=max(df['WEC: ava. reactive Power']),
                        value=20,  # float(temp_val)
                        showCurrentValue=True,
                        color="#fec036",
                        style={
                            "marginTop": "5%",
                            "marginBottom": "-10%",
                            "display": "flex"
                        },
                    ),
                    style={
                        "backgroundColor": "black",
                        "border-radius": "1px",
                        "border-width": "5px",
                        "border-top": "1px solid rgb(216, 216, 216)",
                    },
                )
            ],
        ),
    ],
)

app.layout = dbc.Container(
    fluid=True,
    children=[
        logo(app),
        dbc.Row(
            [
                dbc.Col(graphs, width=10),
                dbc.Col(
                    [
                        dbc.Row(dbc.Col(rul_estimation_indicator, width=12)),
                        dbc.Row(dbc.Col(info_box, width=12)),
                        dbc.Row(dbc.Col(get_new_information_button, width=12)),
                        dbc.Row(dbc.Col(predict_button, width=12)),
                    ]
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(active_power_display, width="auto", style={"height": "100%"}),
                dbc.Col(active_power_from_wind_display, width="auto", style={"height": "100%"}),
                dbc.Col(reactive_power_display, width="auto", style={"height": "100%"}),
                dbc.Col(wind_speed_information, width="auto"),
            ],
        ),
    ],
    # style={"height": "100vh"},
)


@app.callback(
    Output("Main-Graph", "figure"),
    [
        Input("feature-dropdown", "value"),  # Can value be called selected_column?
        Input("date-picker", "start_date"),
        Input("date-picker", "end_date"),
    ],
)
def update_graph(selected_column, start_date, end_date):
    if selected_column in list(df):
        if start_date and end_date:
            start_date_object = datetime.strptime(start_date, "%Y-%m-%d")
            end_date_object = datetime.strptime(end_date, "%Y-%m-%d")
            mask = (df["Time"] > start_date_object) & (df["Time"] <= end_date_object)
            df_within_dates = df.loc[mask]
            fig = go.Figure(
                data=[
                    go.Scatter(
                        x=df_within_dates["Time"], y=df_within_dates[selected_column]
                    )
                ]
            )
            fig.update_layout(
                xaxis=dict(
                    showline=False,
                    showgrid=False,
                    showticklabels=True,
                    zeroline=False,
                    gridcolor="#636363",
                    linecolor="rgb(204, 204, 204)",
                    linewidth=2,
                    tickfont=dict(
                        family="Arial",
                        size=12,
                        color="darkgray",
                    ),
                    title=dict(
                        text="Time",
                        font=dict(family="Arial", size=24, color="darkgray"),
                    ),
                ),
                yaxis=dict(
                    showline=False,
                    showgrid=False,
                    showticklabels=True,
                    zeroline=False,
                    gridcolor="#636363",
                    linecolor="rgb(204, 204, 204)",
                    linewidth=2,
                    tickfont=dict(
                        family="Arial",
                        size=12,
                        color="darkgray",
                    ),
                    title=dict(
                        text=selected_column,
                        font=dict(family="Arial", size=24, color="darkgray"),
                    ),
                ),
                autosize=True,
                margin=dict(autoexpand=True, l=50, b=40, r=35, t=30),
                showlegend=False,
                paper_bgcolor="#2b2b2b",  # plot_bgcolor="#2b2b2b",
                plot_bgcolor="#2b2b2b",  # paper_bgcolor="#2b2b2b",
                title=dict(
                    text=selected_column,
                    font=dict(family="Arial", size=32, color="darkgray"),
                    xanchor="center",
                    yanchor="top",
                    y=1,
                    x=0.5,
                ),
            )
            return fig
        elif start_date:
            start_date_object = datetime.strptime(start_date, "%Y-%m-%d")
            mask = df["Time"] > start_date_object
            df_within_dates = df.loc[mask]
            fig = go.Figure(
                data=[
                    go.Scatter(
                        x=df_within_dates["Time"], y=df_within_dates[selected_column]
                    )
                ]
            )
            fig.update_layout(
                xaxis=dict(
                    showline=False,
                    showgrid=False,
                    showticklabels=True,
                    zeroline=False,
                    gridcolor="#636363",
                    linecolor="rgb(204, 204, 204)",
                    linewidth=2,
                    tickfont=dict(
                        family="Arial",
                        size=12,
                        color="darkgray",
                    ),
                    title=dict(
                        text="Time",
                        font=dict(family="Arial", size=24, color="darkgray"),
                    ),
                ),
                yaxis=dict(
                    showline=False,
                    showgrid=False,
                    showticklabels=True,
                    zeroline=False,
                    gridcolor="#636363",
                    linecolor="rgb(204, 204, 204)",
                    linewidth=2,
                    tickfont=dict(
                        family="Arial",
                        size=12,
                        color="darkgray",
                    ),
                    title=dict(
                        text=selected_column,
                        font=dict(family="Arial", size=24, color="darkgray"),
                    ),
                ),
                autosize=True,
                margin=dict(autoexpand=True, l=50, b=40, r=35, t=30),
                showlegend=False,
                paper_bgcolor="#2b2b2b",  # plot_bgcolor="#2b2b2b",
                plot_bgcolor="#2b2b2b",  # paper_bgcolor="#2b2b2b",
                title=dict(
                    text=selected_column,
                    font=dict(family="Arial", size=32, color="darkgray"),
                    xanchor="center",
                    yanchor="top",
                    y=1,
                    x=0.5,
                ),
            )
            return fig
        else:
            fig = go.Figure(data=[go.Scatter(x=df["Time"], y=df[selected_column])])
            fig.update_layout(
                xaxis=dict(
                    showline=False,
                    showgrid=False,
                    showticklabels=True,
                    zeroline=False,
                    gridcolor="#636363",
                    linecolor="rgb(204, 204, 204)",
                    linewidth=2,
                    tickfont=dict(
                        family="Arial",
                        size=12,
                        color="darkgray",
                    ),
                    title=dict(
                        text="Time",
                        font=dict(family="Arial", size=24, color="darkgray"),
                    ),
                ),
                yaxis=dict(
                    showline=False,
                    showgrid=False,
                    showticklabels=True,
                    zeroline=False,
                    gridcolor="#636363",
                    linecolor="rgb(204, 204, 204)",
                    linewidth=2,
                    tickfont=dict(
                        family="Arial",
                        size=12,
                        color="darkgray",
                    ),
                    title=dict(
                        text=selected_column,
                        font=dict(family="Arial", size=24, color="darkgray"),
                    ),
                ),
                autosize=True,
                margin=dict(autoexpand=True, l=50, b=40, r=35, t=30),
                showlegend=False,
                paper_bgcolor="#2b2b2b",  # plot_bgcolor="#2b2b2b",
                plot_bgcolor="#2b2b2b",  # paper_bgcolor="#2b2b2b",
                title=dict(
                    text=selected_column,
                    font=dict(family="Arial", size=32, color="darkgray"),
                    xanchor="center",
                    yanchor="top",
                    y=1,
                    x=0.5,
                ),
            )
            return fig
    else:
        fig = go.Figure()
        fig.update_layout(
            xaxis=dict(
                showline=False,
                showgrid=False,
                showticklabels=True,
                zeroline=False,
                gridcolor="#636363",
                linecolor="rgb(204, 204, 204)",
                linewidth=2,
                tickfont=dict(
                    family="Arial",
                    size=12,
                    color="darkgray",
                ),
                title=dict(
                    text="Time",
                    font=dict(family="Arial", size=24, color="darkgray"),
                ),
            ),
            yaxis=dict(
                showline=False,
                showgrid=False,
                showticklabels=True,
                zeroline=False,
                gridcolor="#636363",
                linecolor="rgb(204, 204, 204)",
                linewidth=2,
                tickfont=dict(
                    family="Arial",
                    size=12,
                    color="darkgray",
                ),
                title=dict(
                    text=selected_column,
                    font=dict(family="Arial", size=24, color="darkgray"),
                ),
            ),
            autosize=True,
            margin=dict(autoexpand=True, l=50, b=40, r=35, t=30),
            showlegend=False,
            paper_bgcolor="#2b2b2b",  # plot_bgcolor="#2b2b2b",
            plot_bgcolor="#2b2b2b",  # paper_bgcolor="#2b2b2b",
            title=dict(
                text=selected_column,
                font=dict(family="Arial", size=32, color="darkgray"),
                xanchor="center",
                yanchor="top",
                y=1,
                x=0.5,
            ),
        )
        return fig


@app.callback(
    [Output('active-power-information-gauge', 'value'),
     Output('active-power-from-wind-information-gauge', 'value'),
     Output('wind-power-information-gauge', 'value'),
     Output('reactive-power-information-gauge', 'value')],
    Input('Main-Graph', 'clickData')
)
def display_click_data(clickData):
    if clickData:
        data_time = clickData['points'][0]['x']
        value_active_power = df['WEC: ava. Power'].loc[df['Time'] == data_time].values[0]
        value_active_power_wind = df['WEC: ava. available P from wind'].loc[df['Time'] == data_time].values[0]
        value_reactive_power = df['WEC: ava. reactive Power'].loc[df['Time'] == data_time].values[0]
        value_wind_speed = df['WEC: ava. windspeed'].loc[df['Time'] == data_time].values[0]
        return value_active_power, value_active_power_wind, value_wind_speed, value_reactive_power
    else:
        value_active_power = 0
        value_active_power_wind = 0
        value_reactive_power = 0
        value_wind_speed = 0
        return value_active_power, value_active_power_wind, value_wind_speed, value_reactive_power


if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=True)

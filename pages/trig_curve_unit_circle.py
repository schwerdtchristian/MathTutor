import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import numpy as np

dash.register_page(__name__)
layout = html.Div([
    html.H4('Sinus curve vs. unit circle visualization'),
    dcc.Graph(id="sin_curve_unity"),
    dcc.Graph(id="unity_circle"),
    html.P(id = "sin_value"),
    html.P("Angle"),
    html.Button("-", n_clicks=0, id='btn-dec', style={'font-size': '18px', 'width': '140px', 'height':'30px'}),
    html.Button("+", n_clicks=0, id='btn-inc', style={'font-size': '18px', 'width': '140px', 'height':'30px'}),
    ])


@callback(Output("sin_curve_unity", "figure"), Input("btn-dec", "n_clicks"), Input("btn-inc", "n_clicks"))
def draw_sin_curve(n_left, n_right):
    n = 0.1 * (n_right - n_left)
    x = np.linspace(-2*np.pi, 2*np.pi, 100)
    y = np.sin(x)

    trace1 = go.Scatter(
        x=x,
        y=y,
        mode='lines',
    )

    trace2 = go.Scatter(
        x = [n],
        y = [np.sin(n)]
    )
    trace_data = [trace1, trace2]
    fig = go.Figure(data=trace_data)
    fig.update_layout(showlegend=False, title =  "Sinus curve", title_x = 0.5)

    return fig

@callback(Output("unity_circle", "figure"), Input("btn-dec", "n_clicks"), Input("btn-inc", "n_clicks"))
def draw_unity_circle(n_left, n_right):
    n = 0.1 * (n_right - n_left)
    x = np.cos(n)
    y = np.sin(n)

    trace1 = go.Scatter(
        x=[0, x],
        y=[0, y],
    )

    x1 = np.linspace(-1, 1, 100)
    y1 = np.sqrt(1 - x1*x1)
    trace2 = go.Scatter(
        x = x1,
        y = y1,
        mode = "lines"
    )

    x2 = np.linspace(-1, 1, 100)
    y2 = -np.sqrt(1 - x2*x2)
    trace3 = go.Scatter(
        x = x2,
        y = y2,
        mode = "lines"
    )

    trace_data = [trace1, trace2, trace3]
    fig = go.Figure(data=trace_data)
    fig.update_xaxes(range=[-1.5, 1.5])
    fig.update_yaxes(range=[-1.5, 1.5])
    fig.update_layout(autosize = False, width = 500, height = 500, showlegend=False, title =  "Unit circle", title_x = 0.5)

    return fig

@callback(Output("sin_value", "children"), Input("btn-dec", "n_clicks"), Input("btn-inc", "n_clicks"))
def area_formula(n_left, n_right):
    n = 0.1 * (n_right - n_left)
    return np.sin(n)

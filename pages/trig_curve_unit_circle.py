import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import numpy as np

dash.register_page(module = __name__, name = "Connection between sinus function graph and unit circle")

layout = html.Div([
    html.H4('Sinus curve vs. unit circle visualization', style={"font-size": "30px", "text-align": "center"}),
    html.P("Explore how the graph of the sinus function is connected with the unit circle by changing the angle (v) measured in radians. Explore how the y value on the y axis is alternating between -1 and 1 in both the sinus function graph and unity circle when increasing the angle (v)", style={"text-align": "center"}),
    dcc.Graph(id="sin_curve_unity"),
    dcc.Graph(id="unity_circle"),
    html.P("Angle (v)"),
    html.Button("-", n_clicks=0, id='btn-dec', style={'font-size': '18px', 'width': '140px', 'height':'30px'}),
    html.Button("+", n_clicks=0, id='btn-inc', style={'font-size': '18px', 'width': '140px', 'height':'30px'}),
    html.P("Created by Christian Schwerdt", style={"font-style": "italic", "text-align": "right"}),
    ])


@callback(Output("sin_curve_unity", "figure"), Input("btn-dec", "n_clicks"), Input("btn-inc", "n_clicks"))
def draw_sin_curve(n_left, n_right):
    n = 0.1 * (n_right - n_left)
    x = np.linspace(-2*np.pi, 2*np.pi, 100)
    y = np.sin(x)

    point = go.Scatter(
        x=x,
        y=y,
        mode='lines',
    )

    y_level = go.Scatter(
        x = [n],
        y = [np.sin(n)] 
    )

    x_level = go.Scatter(
        x = [0, n],
        y = [np.sin(n), np.sin(n)],
        line = {"dash":"dash"},
        mode = "lines + text",
        text = [f"sin(v) = {np.round(np.sin(n), 2)}"],
        textposition = "top right" 
    )

    sin_curve = go.Scatter(
        x = [n, n],
        y = [0, np.sin(n)],
        line = {"dash":"dash"},
        mode = "lines + text",
        text = [f"v = {np.round(n,2)}"],
        textposition = "bottom right" 
    )

    trace_data = [point, y_level, x_level, sin_curve]
    fig = go.Figure(data=trace_data)
    fig.update_layout(showlegend=False, title =  "Sinus function graph", title_x = 0.5, xaxis_title="angle (v)", yaxis_title="sin(v)")
    fig.update_traces (marker_size = 12)

    return fig

@callback(Output("unity_circle", "figure"), Input("btn-dec", "n_clicks"), Input("btn-inc", "n_clicks"))
def draw_unity_circle(n_left, n_right):
    n = 0.1 * (n_right - n_left)
    x = np.cos(n)
    y = np.sin(n)

    point = go.Scatter(
        x=[0, x],
        y=[0, y],
    )

    y_level = go.Scatter(
        x = [0, x],
        y = [y, y],
        line = {"dash":"dash"},
        mode = "lines + text",
        text = [f"sin(v) = {np.round(np.sin(n), 2)}"],
        textposition = "top right" 
    )

    trace_data = [point, y_level]
    fig = go.Figure(data=trace_data)
    
    fig.add_shape(type="circle",
    xref="x", yref="y",
    x0=-1, y0=-1, x1=1, y1=1,
    line_color="LightSeaGreen",
    )

    fig.update_xaxes(range=[-1.5, 1.5])
    fig.update_yaxes(range=[-1.5, 1.5])
    fig.update_layout(autosize = False, width = 500, height = 500, showlegend=False, title =  "Unit circle", title_x = 0.5)
    fig.add_annotation(x = x/3, y = y/3,
                       text = f"v = {np.round(n, 2)}",
                       showarrow = False,
                       yshift = 0)

    return fig

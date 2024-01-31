import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import numpy as np

dash.register_page(module = __name__, name = "Find both angles for sin and cos in unity circle")

layout = html.Div([
    html.H4('Visualize both angles giving the same sin or cos value', style={"font-size": "30px", "text-align": "center"}),
    html.P("Explore how two angles give the same sin or cos value respectively. These two angles are a subset of all possible values which can be explored more on the sinus equation page", style={"text-align": "center"}),
    dcc.Graph(id="unity_circle2"),
    html.P("Angle (v)"),
    html.Button("-", n_clicks=0, id='btn-dec', style={'font-size': '18px', 'width': '140px', 'height':'30px'}),
    html.Button("+", n_clicks=0, id='btn-inc', style={'font-size': '18px', 'width': '140px', 'height':'30px'}),
    html.P("Created by Christian Schwerdt", style={"font-style": "italic", "text-align": "right"}),
    ])



@callback(Output("unity_circle2", "figure"), Input("btn-dec", "n_clicks"), Input("btn-inc", "n_clicks"))
def draw_unity_circle(n_left, n_right):
    n = 0.1 * (n_right - n_left)
    x = np.cos(n)
    y = np.sin(n)

    point = go.Scatter(
        x=[0, x],
        y=[0, y],
    )

    point_sin_2 = go.Scatter(
        x=[0, -x],
        y=[0, y],
    )

    point_cos_2 = go.Scatter(
        x=[0, x],
        y=[0, -y],
    )

    y_level = go.Scatter(
        x = [-x, x],
        y = [y, y],
        line = {"dash":"dash"},
        mode = "lines + text",
        text = [f"sin(v) = {np.round(np.sin(n), 2)}"],
        textposition = "top right" 
    )

    x_level = go.Scatter(
        x = [x, x],
        y = [-y, y],
        line = {"dash":"dash"},
        mode = "lines + text",
        text = [f"cos(v) = {np.round(np.cos(n), 2)}"],
        textposition = "top right" 
    )

    trace_data = [point, point_sin_2, point_cos_2, y_level, x_level]
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
    fig.add_annotation(x = -x/3, y = y/3,
                       text = f"v = {np.round(np.pi - n, 2)}",
                       showarrow = False,
                       yshift = 0)
    fig.add_annotation(x = x/3, y = -y/3,
                       text = f"v = {np.round(-n, 2)}",
                       showarrow = False,
                       yshift = 0)

    return fig
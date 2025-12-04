import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import numpy as np

dash.register_page(module = __name__, name = "Area and primitive function")
layout = html.Div([
     html.H4('Area and primitive function', style={"font-size": "30px", "text-align": "center"}), 
     html.P("Explore how the area under a function can be determined by the value of its primitive function. By using the buttons the area under Function A can be increased, decreased or stay the same. Notice how the value of the primitive to function A reflects this, ecpecially notice that if the area under Function A stays the same the primitive of Function A is horizontal hence its derivitive (meaning Function A) is zero", style={"text-align": "center"}),
     html.Div([

        # LEFT COLUMN — BUTTONS STACKED VERTICALLY
        html.Div([
            html.Button("Increase area", n_clicks=0, id='btn-incArea',
                        style={'font-size': '18px', 'width': '140px', 'height':'50px', 'marginBottom': '10px'}),

            html.Button("Same area", n_clicks=0, id='btn-sameArea',
                        style={'font-size': '18px', 'width': '140px', 'height':'50px', 'marginBottom': '10px'}),

            html.Button("Decrease area", n_clicks=0, id='btn-decArea',
                        style={'font-size': '18px', 'width': '140px', 'height':'50px'})
        ],
        style={
            "display": "flex",
            "flexDirection": "column",
            "marginRight": "30px"  # space between buttons and graphs
        }),

        # RIGHT COLUMN — THE TWO GRAPHS STACKED VERTICALLY
        html.Div([
            dcc.Graph(id="derivative_function", style={"height": "300px"}),
            dcc.Graph(id="primitive_function", style={"height": "300px"}),
        ],
        style={
            "display": "flex",
            "flexDirection": "column",
            "width": "100%",     # optional: keep graphs bigger
        })

    ],
    style={
        "display": "flex",
        "flexDirection": "row",    # buttons LEFT, graphs RIGHT (side by side)
        "alignItems": "center"
    }), 
     html.P(id = "area_calculation_primitive_function"), 
     dcc.Store(id = "prev_y_prim"),
     html.P("Created by Christian Schwerdt", style={"font-style": "italic", "text-align": "right"}),
     ])


@callback(Output("primitive_function", "figure"), Output("prev_y_prim", "data"), Input("prev_y_prim", "data"), Input("btn-decArea", "n_clicks"), Input("btn-sameArea", "n_clicks"), Input("btn-incArea", "n_clicks"))
def draw_primitive_function(data, n_decArea, n_sameArea, n_incArea):
    n = (n_incArea - n_decArea + 0*n_sameArea)
    if not data:
         y = [0]
         x = [0]
         x_axis_length = 1
    else:
        y = data + [n]
        x = [x for x in range(len(y))]
        x_axis_length = len(data) + 1
    fig = go.Figure(go.Scatter(
        x = x, y=y,
    ), layout = {"title": "Primitive of function A", "title_x" : 0.5, "yaxis_title" : "Area of function A"})
    fig.update_xaxes(range=[0, x_axis_length])

    return fig, y

@callback(Output("derivative_function", "figure"), Input("prev_y_prim", "data"))
def draw_derivative_function(data):
    if not data or len(data) == 1:
         y = [0]
         x = [0]
         x_axis_length = 1
    elif len(data) == 2:
        y_temp = np.diff(data)
        y = np.append(y_temp, y_temp[-1])
        x = [x for x in range(len(y))]
        x_axis_length = len(data)
    else:
        diffs = np.diff(data)
        y = np.array([diffs[0], diffs[0]])
        x = np.array([0, 1])
        for index in range(len(diffs) - 1):
             y = np.append(y, np.array([diffs[index + 1], diffs[index + 1]]))
             x = np.append(x, np.array([index + 1, index + 2]))
        x_axis_length = len(data)
    fig = go.Figure(go.Scatter(
        x = x, y = y,
        fill = "tozeroy",
    ), layout = {"title": "Function A", "title_x" : 0.5})
    fig.update_xaxes(range=[0, x_axis_length])

    return fig


@callback(Output("area_calculation_primitive_function", "children"), Input("btn-left", "n_clicks"), Input("btn-right", "n_clicks"))
def area_formula(n_left, n_right):
        return "Area under derivative function equals primitive function"
    
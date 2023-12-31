import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import numpy as np

dash.register_page(module = __name__, name = "Connection between area and primitive function")
layout = html.Div([
     html.H4('Primitive function as area function', style={"font-size": "30px", "text-align": "center"}), 
     html.P("Explore how the primitive function can be intepreted as the area of its derivative function. By clicking on the button to add area the primitive function is increasing its value while the area under the curve for the derivative function increases and vice versa when the button for decreasing the area is clicked. Ecpecially note that to keep the area constant means that the primitive function needs to horizontal, meaning that its derivative is zero hence its derivative function graph is zero", style={"text-align": "center"}),
     dcc.Graph(id="primitive_function"),
     dcc.Graph(id="derivative_function"), 
     html.Button("Decrease area", n_clicks=0, id='btn-decArea', style={'font-size': '18px', 'width': '140px', 'height':'50px'}), 
     html.Button("Same area", n_clicks=0, id='btn-sameArea', style={'font-size': '18px', 'width': '140px', 'height':'50px'}), 
     html.Button("Increase area", n_clicks=0, id='btn-incArea', style={'font-size': '18px', 'width': '140px', 'height':'50px'}), 
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
    ), layout = {"title": "primitive function - area function", "title_x" : 0.5})
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
    ), layout = {"title": "derivative function", "title_x" : 0.5})
    fig.update_xaxes(range=[0, x_axis_length])

    return fig


@callback(Output("area_calculation_primitive_function", "children"), Input("btn-left", "n_clicks"), Input("btn-right", "n_clicks"))
def area_formula(n_left, n_right):
        return "Area under derivative function equals primitive function"
    
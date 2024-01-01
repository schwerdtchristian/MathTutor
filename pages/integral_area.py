import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go

#app = Dash(__name__)
dash.register_page(__name__)
layout = html.Div([html.H4('Primitive function as area function'), dcc.Graph(id="primitive_function"),dcc.Graph(id="derivative_function"), html.Button("Decrease area", n_clicks=0, id='btn-decArea'), html.Button("Increase area", n_clicks=0, id='btn-incArea'), html.P(id = "area_calculation_primitive_function")])


@callback(Output("primitive_function", "figure"), Input("btn-decArea", "n_clicks"), Input("btn-incArea", "n_clicks"))
def draw_primitive_function(n_decArea, n_incArea):
    n = (n_incArea - n_decArea)
    fig = go.Figure(go.Scatter(
        x = [0, 1], y=[0, n],
        fill = "toself",
    ), layout = {"title": "primitive function - area function"})
    fig.update_xaxes(range=[-2, 4])

    return fig

@callback(Output("derivative_function", "figure"), Input("btn-decArea", "n_clicks"), Input("btn-incArea", "n_clicks"))
def draw_derivative_function(n_decArea, n_incArea):
    n = (n_incArea - n_decArea)
    fig = go.Figure(go.Scatter(
        x = [0, 0, 1, 1, 0], y=[0, n, n, 0, 0],
        fill = "toself",
    ), layout = {"title": "derivative function"})
    fig.update_xaxes(range=[-2, 4])

    return fig


@callback(Output("area_calculation_primitive_function", "children"), Input("btn-left", "n_clicks"), Input("btn-right", "n_clicks"))
def area_formula(n_left, n_right):
        return "Area under derivative function equals primitive function"
    
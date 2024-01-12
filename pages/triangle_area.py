import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go

dash.register_page(module = __name__, name = "Triangle area")
layout = html.Div([
    html.H4('Triangle area formula', style={"font-size": "30px", "text-align": "center"}),
    html.P("Explore the triangle area formula and see why the area formula stays the same regardless of the shape of the triangle. The triangle area is calculated by creating two sub triangles which areas are added or subtracted depending on the shape of the original triangle, but the triangle area formula stays the same.", style={"text-align": "center"}),
    dcc.Graph(id="triangle"),
    html.Div(children = [
        dcc.Graph(id="sub_triangle1", style = {"display" : "inline-block"}),
        dcc.Graph(id="sub_triangle2", style = {"display" : "inline-block"}),
    ]),
    html.P(id = "area_calculations"),
    html.B("Area = b * h / 2"),
    html.Div([
        html.Button("Move A left", n_clicks=0, id='btn-left', style={'font-size': '18px', 'width': '140px', 'height':'50px', 'margin-top': '20px'}),
        html.Button("Move A right", n_clicks=0, id='btn-right', style={'font-size': '18px', 'width': '140px', 'height':'50px'})]),
    html.P("Created by Christian Schwerdt", style={"font-style": "italic", "text-align": "right"}),
    ])

@callback(Output("triangle", "figure"), Input("btn-left", "n_clicks"), Input("btn-right", "n_clicks"))
def draw_triangle(n_left, n_right):
    n = 0.5*(n_right - n_left)
    fig = go.Figure(go.Scatter(
        x = [1+n, 0, 2, 1+n, 1+n, 1+n], y=[2, 0, 0, 2, 0, 2],
        fill = "toself",
        mode = "lines + text",
        text = ["A", "B", "D", "A", "C"],
        textfont = {"size":20},
    ), layout = {"title": "Triangle", "title_x" : 0.5})
    fig.update_xaxes(range=[min(n - 1, -1), max(n + 2, 3)], visible = False)
    fig.update_yaxes(visible = False)
    fig.add_annotation(x = 1, y = -0.2,
                       text = "b",
                       showarrow = False,
                       yshift = 0)
    fig.add_annotation(x = 1.05 + n, y = 1,
                       text = "h",
                       showarrow = False,
                       yshift = 0)

    return fig

@callback(Output("sub_triangle1", "figure"), Input("btn-left", "n_clicks"), Input("btn-right", "n_clicks"))
def draw_sub_triangle1(n_left, n_right):
    n = 0.5*(n_right - n_left)
    fig = go.Figure(go.Scatter(
        x = [1+n, 0, 1+n, 1+n], y=[2, 0, 0, 2],
        fill = "toself",
        mode = "lines + text",
        text = ["A", "B", "C"],
        textfont = {"size":20},
    ), layout = {"title": "Triangle 1", "title_x" : 0.5})
    fig.update_xaxes(range=[min(n - 1, -1), max(n + 2, 2)], visible = False)
    fig.update_yaxes(visible = False)
    fig.add_annotation(x = 0.5 + n/2, y = -0.2,
                       text = "b1",
                       showarrow = False,
                       yshift = 0)
    fig.add_annotation(x = 1.1 + n, y = 1,
                       text = "h",
                       showarrow = False,
                       yshift = 0)

    return fig

@callback(Output("sub_triangle2", "figure"), Input("btn-left", "n_clicks"), Input("btn-right", "n_clicks"))
def draw_sub_triangle2(n_left, n_right):
    n = 0.5*(n_right - n_left)
    fig = go.Figure(go.Scatter(
        x = [1+n, 1+n, 2, 1+n], y=[2, 0, 0, 2],
        fill = "toself",
        mode = "lines + text",
        text = ["A", "C", "D"],
        textfont = {"size":20},
    ), layout = {"title": "Triangle 2", "title_x" : 0.5})
    fig.update_xaxes(range=[min(n - 1, -1), max(n + 2, 3)], visible = False)
    fig.update_yaxes(visible = False)
    fig.add_annotation(x = 1.5 + n/2, y = -0.2,
                       text = "b2",
                       showarrow = False,
                       yshift = 0)
    fig.add_annotation(x = 0.90 + n, y = 1,
                       text = "h",
                       showarrow = False,
                       yshift = 0)

    return fig

@callback(Output("area_calculations", "children"), Input("btn-left", "n_clicks"), Input("btn-right", "n_clicks"))
def area_formula(n_left, n_right):
    n = 0.5*(n_right - n_left)
    if n > -1 and n < 1:
        return "Triangle area = Triangle 1 area + Triangle 2 area = (b1 * h) / 2 + (b2 * h) / 2 = (b1 + b2) * h / 2 = (b * h ) / 2 "
    elif n == -1:
        return "Triangle area = Triangel 2 area = (b2 * h ) / 2 = (b * h) / 2"
    elif n == 1:
        return "Triangle area = Triangle 1 area = (b1 * h) / 2 = (b * h) / 2 "
    elif n < -1:
        return "Triangle area = Triangle 2 area - Triangle 1 area = (b2 * h) / 2 - (b1 * h) / 2 = (b2 - b1) * h / 2 = (b * h) / 2"
    elif n > 1:
        return "Triangle area = Triangle 1 area - Triangle 2 area = (b1 * h) / 2 - (b2 * h) / 2 = (b1 - b2) * h / 2 = (b * h) / 2"
    
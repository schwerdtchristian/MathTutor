from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go

app = Dash(__name__)

app.layout = html.Div([html.H4('Live data control'), dcc.Graph(id="triangle"),dcc.Graph(id="sub_triangle1"), dcc.Graph(id="sub_triangle2"), html.P(id = "area_calculations"), html.P("Area = b * h / 2"), html.Button("Move left", n_clicks=0, id='btn-left'), html.Button("Move right", n_clicks=0, id='btn-right'),])


@app.callback(Output("triangle", "figure"), Input("btn-left", "n_clicks"), Input("btn-right", "n_clicks"))
def draw_traingle(n_left, n_right):
    n = 0.5*(n_right - n_left)
    fig = go.Figure(go.Scatter(
        x = [1+n, 0, 2, 1+n, 1+n, 1+n], y=[2, 0, 0, 2, 0, 2],
        fill = "toself",
    ), layout = {"title": "Triangle"})
    fig.update_xaxes(range=[-2, 4])

    return fig

@app.callback(Output("sub_triangle1", "figure"), Input("btn-left", "n_clicks"), Input("btn-right", "n_clicks"))
def draw_sub_triangle1(n_left, n_right):
    n = 0.5*(n_right - n_left)
    fig = go.Figure(go.Scatter(
        x = [1+n, 0, 1+n, 1+n], y=[2, 0, 0, 2],
        fill = "toself",
    ), layout = {"title": "Triangle 1"})
    fig.update_xaxes(range=[-2, 4])

    return fig

@app.callback(Output("sub_triangle2", "figure"), Input("btn-left", "n_clicks"), Input("btn-right", "n_clicks"))
def draw_sub_triangle2(n_left, n_right):
    n = 0.5*(n_right - n_left)
    fig = go.Figure(go.Scatter(
        #x = [0, 1+n, 1+n], y=[0, 0, 2],
        x = [1+n, 1+n, 2, 1+n], y=[2, 0, 0, 2],
        fill = "toself",
    ), layout = {"title": "Triangle 2"})
    fig.update_xaxes(range=[-2, 4])

    return fig

@app.callback(Output("area_calculations", "children"), Input("btn-left", "n_clicks"), Input("btn-right", "n_clicks"))
def area_formula(n_left, n_right):
    n = 0.5*(n_right - n_left)
    if n > -1 and n < 1:
        return "Total triangle area is triangle area 1 + triangle area 2. Area = (b1 * h) / 2 + (b2 * h) / 2 = (b * h ) / 2 "
    elif n == -1:
        return "Total area is triangle area 2. Area = (b2 * h ) / 2 = (b * h) / 2"
    elif n == 1:
        return "Total area is triangle area 1. Area = (b1 * h) / 2 = (b * h) / 2 "
    elif n < -1:
        return "Total area is triangle area 2 - triangle area 1 = (b2 * h) / 2 - (b1 * h) / 2 = (b2 - b1) * h / 2 = (b * h) / 2"
    elif n > 1:
        return "Total area is triangle area 1 - triangle area 2. Area = (b1 * h) / 2 - (b2 * h) / 2 = (b1 - b2) * h / 2 = (b * h) / 2"
    


app.run_server(debug=True)
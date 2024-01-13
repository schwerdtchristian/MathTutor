import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import numpy as np

dash.register_page(module = __name__, name = "Percent")

layout = html.Div([
    html.H4('Percent', style={"font-size": "30px", "text-align": "center"}),
    html.P("Percent means one part in hundred of something. One percent of something is if you divide that thing in hundred equals parts and take one of those parts. Similarly 5 percent of something is that you divide that thing in hundred equal parts and take five of those parts. Usually questions about procetn can be written as: start amount + percent change = new amount. Lets explore how it looks visually", style={"text-align": "center"}),
    html.B("Known start amount and percent change", style={"font-size": "30px"}),
    html.P(id = "start amount numerical", style={"font-size": "30px"}),
    html.P(id = "percent change", style={"font-size": "30px"}),
    html.P(id = "change amount numerical", style={"font-size": "30px"}),
    html.P(id = "end amount numerical", style={"font-size": "30px"}),
    dcc.Graph(id="start and end amount"),
    html.Div([
        html.P("Start amount"),
        html.Button("-", n_clicks=0, id='btn-decStart', style={'font-size': '18px', 'width': '140px', 'height':'30px', 'margin-bottom': '20px'}),
        html.Button("+", n_clicks=0, id='btn-incStart', style={'font-size': '18px', 'width': '140px', 'height':'30px', 'margin-bottom': '20px'})]), 
    html.Div([
        html.P("Percent"),
        html.Button("-", n_clicks=0, id='btn-decPercent', style={'font-size': '18px', 'width': '140px', 'height':'30px', 'margin-bottom': '20px'}),
        html.Button("+", n_clicks=0, id='btn-incPercent', style={'font-size': '18px', 'width': '140px', 'height':'30px', 'margin-bottom': '20px'})]), 
    html.P("Created by Christian Schwerdt", style={"font-style": "italic", "text-align": "right"}),
        ])


@callback(Output("start and end amount", "figure"), Input("btn-decStart", "n_clicks"), Input("btn-incStart", "n_clicks"), Input("btn-decPercent", "n_clicks"), Input("btn-incPercent", "n_clicks"))
def draw_start_amount(n_decStart, n_incStart, n_decPercent, n_incPercent):
    n_start = 100 + (n_incStart - n_decStart)
    n_percent = 0 + (n_incPercent - n_decPercent)

    trace1 = go.Scatter(
        x = [0, 0, n_start, n_start, 0],
        y = [5, 10, 10, 5, 5],
        fill = "toself",
        mode = "lines + text",
    )

    trace2 = go.Scatter(
        x = [0, 0, n_start * (1 + n_percent/100), n_start * (1 + n_percent/100), 0],
        y = [-5, -10, -10, -5, -5],
        fill = "toself",
        mode = "lines + text",
    )

    trace3 = go.Scatter(
        x = [n_start, n_start * (1 + n_percent/100)],
        y = [0, 0],
        line = {"dash":"dash"},
        mode = "lines"
    )

    trace_data = [trace1, trace2, trace3]
    fig = go.Figure(data=trace_data)
    fig["data"][0]["name"] = "start amount"
    fig["data"][1]["name"] = "end amount"
    fig["data"][2]["name"] = "change amount"
    fig.update_layout(showlegend=True)
    fig.update_yaxes(range=[-12, 12])
    fig.update_xaxes(range=[min(-1, n_start * (1 + n_percent/100) - 1), max(n_start * (1 + n_percent/100) + 1, n_start + 1)])
    fig.update_yaxes(visible = False)

    return fig

@callback(Output("start amount numerical", "children"), Input("btn-decStart", "n_clicks"), Input("btn-incStart", "n_clicks"))
def start_amount(n_decStart, n_incStart):
    n_start = 100 + (n_incStart - n_decStart)
    return f"Start amount: {n_start}"

@callback(Output("percent change", "children"), Input("btn-decPercent", "n_clicks"), Input("btn-incPercent", "n_clicks"))
def percent_change(n_decPercent, n_incPercent):
    n_percent = 0 + (n_incPercent - n_decPercent)
    return f"Percent change: {n_percent}"

@callback(Output("end amount numerical", "children"), Input("btn-decStart", "n_clicks"), Input("btn-incStart", "n_clicks"), Input("btn-decPercent", "n_clicks"), Input("btn-incPercent", "n_clicks"))
def end_amount(n_decStart, n_incStart, n_decPercent, n_incPercent):
    n_start = 100 + (n_incStart - n_decStart)
    n_percent = 0 + (n_incPercent - n_decPercent)
    n_end = n_start * (1 + n_percent/100)
    return f"End amount: start amount + change amount = {n_start} + {n_start} / 100 * {n_percent} = {n_start} * (1 + {n_percent}/100) = {n_end}"

@callback(Output("change amount numerical", "children"), Input("btn-decStart", "n_clicks"), Input("btn-incStart", "n_clicks"), Input("btn-decPercent", "n_clicks"), Input("btn-incPercent", "n_clicks"))
def change_amount(n_decStart, n_incStart, n_decPercent, n_incPercent):
    n_start = 100 + (n_incStart - n_decStart)
    n_percent = 0 + (n_incPercent - n_decPercent)
    return f"Change amount: start amount / 100 * how many percent = {n_start} / 100 * {n_percent} = {n_start / 100 * n_percent}"

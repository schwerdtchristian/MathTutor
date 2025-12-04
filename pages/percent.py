import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go

dash.register_page(module = __name__, name = "Percent")

layout = html.Div([
    html.H4('Percent', style={"font-size": "30px", "text-align": "center"}),
    html.P("Percent means per hundred, or one part per hundred total parts. So one percent of something is if you divide that thing in hundred equal parts and take one of those parts. Similarly 5 percent of something is that you divide that thing in hundred equal parts and take five of those parts. Lets explore how it looks visually. Try for example to increase a start value with 10% and then decrease the new value (by using the new value as the start value) with 10%. Will the final end value be the same as the start value you started with?", style={"text-align": "center"}),
    html.P(id = "start amount numerical", style={"font-size": "12px"}),
    html.P(id = "percent change", style={"font-size": "12px"}),
    html.P(id = "change amount numerical", style={"font-size": "12px"}),
    html.P(id = "end amount numerical", style={"font-size": "12px"}),
    dcc.Graph(id="start and end amount"),
    html.Div([
        html.P("Start amount"),
        html.Button("-", n_clicks=0, id='btn-decStart', style={'font-size': '18px', 'width': '140px', 'height':'30px', 'margin-bottom': '20px'}),
        html.Button("+", n_clicks=0, id='btn-incStart', style={'font-size': '18px', 'width': '140px', 'height':'30px', 'margin-bottom': '20px'})]), 
    html.Div([
        html.P("Percent change"),
        html.Button("-", n_clicks=0, id='btn-decPercent', style={'font-size': '18px', 'width': '140px', 'height':'30px', 'margin-bottom': '20px'}),
        html.Button("+", n_clicks=0, id='btn-incPercent', style={'font-size': '18px', 'width': '140px', 'height':'30px', 'margin-bottom': '20px'})]), 
    html.P("Created by Christian Schwerdt", style={"font-style": "italic", "text-align": "right"}),
        ])


@callback(
    Output("start and end amount", "figure"),
    Input("btn-decStart", "n_clicks"), 
    Input("btn-incStart", "n_clicks"),
    Input("btn-decPercent", "n_clicks"), 
    Input("btn-incPercent", "n_clicks")
)
def draw_start_amount(n_decStart, n_incStart, n_decPercent, n_incPercent):

    n_start = 100 + (n_incStart - n_decStart)
    n_percent = (n_incPercent - n_decPercent)
    change_amount = n_start * (n_percent / 100)
    n_end = n_start + change_amount

    # START BAR (top)
    trace1 = go.Scatter(
        x=[0,0,n_start,n_start,0],
        y=[5,10,10,5,5],
        fill="toself",
        mode="lines",
        name="start amount",
        line=dict(color="blue")
    )

    # 🔥 Make dashed line visible: plotted *after* bar, slightly above it
    trace_change_dash = go.Scatter(
        x=[0, change_amount],
        y=[10.2, 10.2],                # subtle offset to make it visible
        mode="lines",
        line=dict(color="black", width=3, dash="dash"),
        name="changed amount"
    )

    # END BAR (bottom)
    trace2 = go.Scatter(
        x=[0,0,n_end,n_end,0],
        y=[-5,-10,-10,-5,-5],
        fill="toself",
        mode="lines",
        name="end amount",
        line=dict(color="orange")
    )

    # Connector dashed line — still visible but not in legend
    trace3 = go.Scatter(
        x=[n_start, n_end],
        y=[0,0],
        mode="lines",
        showlegend=False,
        line=dict(color="black", dash="dash")
    )

    fig = go.Figure([trace1, trace2, trace_change_dash, trace3])

    # ===============================
    # X-AXIS CONFIG — now working
    # ===============================
    fig.update_xaxes(
        tick0=0,
        dtick=10,               # major ticks
        ticklen=10,
        showgrid=True,
        minor=dict(
            dtick=1,            # minor ticks every 1
            showgrid=True,      # required for visibility
            gridwidth=0.5,
        )
    )

    fig.update_yaxes(range=[-12, 12], visible=False)
    fig.update_xaxes(range=[-2, max(n_start, n_end) + 5])
    fig.update_layout(showlegend=True)

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
    return f"Change amount: start amount / 100 * percent changes = {n_start} / 100 * {n_percent} = {n_start / 100 * n_percent}"

import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import numpy as np

dash.register_page(__name__)
layout = html.Div([html.H4('Sinus curve parameters visualization'), dcc.Graph(id="sin_curve_solution"), html.P(id = "sin_equation_solution"), html.Div([html.P("y"), html.Button("-", n_clicks=0, id='btn-decY'), html.Button("+", n_clicks=0, id='btn-incY')]), html.Div([html.P("Amplitude"), html.Button("-", n_clicks=0, id='btn-decAmp'), html.Button("+", n_clicks=0, id='btn-incAmp')]), html.Div([html.P("Frequency"), html.Button("- Freq", n_clicks=0, id='btn-decFreq'), html.Button("+ Freq", n_clicks=0, id='btn-incFreq')]), html.Div([html.P("Phase shift"), html.Button("-", n_clicks=0, id='btn-decPhase'), html.Button("+", n_clicks=0, id='btn-incPhase')]), html.Div([html.P("Function avarage"), html.Button("-", n_clicks=0, id='btn-decCenter'), html.Button("+", n_clicks=0, id='btn-incCenter')])])


@callback(Output("sin_curve_solution", "figure"), Input("btn-decY", "n_clicks"), Input("btn-incY", "n_clicks"), Input("btn-decPhase", "n_clicks"), Input("btn-incPhase", "n_clicks"), Input("btn-decAmp", "n_clicks"), Input("btn-incAmp", "n_clicks"), Input("btn-decFreq", "n_clicks"), Input("btn-incFreq", "n_clicks"), Input("btn-decCenter", "n_clicks"), Input("btn-incCenter", "n_clicks"))
def draw_sin_curve(n_decY, n_incY, n_decPhase, n_incPhase, n_decAmp, n_incAmp, n_decFreq, n_incFreq, n_decCenter, n_incCenter):
    n_phase = 0.1 * (n_incPhase - n_decPhase)
    n_amp = 1 + (n_incAmp - n_decAmp)
    n_freq = 1 + (n_incFreq - n_decFreq)
    n_center = (n_incCenter - n_decCenter)
    x = np.linspace(- 2*2*np.pi, 2*2*np.pi, 100)
    y = n_amp * np.sin(n_freq*x + n_phase) + n_center
    y_const = n_incY - n_decY
    B = 1 + (n_incFreq - n_decFreq)
    x_solution = (np.arcsin((y_const - n_center)/n_amp) - n_phase) / n_freq
    x_solution_2 = (np.pi - np.arcsin((y_const - n_center)/n_amp) - n_phase) / n_freq

    trace1 = go.Scatter(
        x=x,
        y=y,
        mode='lines',
    )

    x2 = [x_solution + 2 * np.pi / B * (n-5) for n in range(10)]
    y2 = [y_const for n in range(10)] 
    trace2 = go.Scatter(
        x = x2,
        y=y2,
    )

    x3 = [x_solution_2 + 2 * np.pi / B * (n-5) for n in range(10)]
    y3 = [y_const for n in range(10)] 
    trace3 = go.Scatter(
        x = x3,
        y=y3,
    )

    trace_data = [trace1, trace2, trace3]
    fig = go.Figure(data=trace_data)
    fig["data"][0]["name"] = "sinus functions"
    fig["data"][1]["name"] = f"x1 + n * 2 * pi / {n_freq}"
    fig["data"][2]["name"] = f"pi - x1 + n * pi / {n_freq}"
    fig.add_hline(y = y_const)
    fig.update_layout(showlegend=True)
    fig.update_yaxes(range=[n_center - 5, n_center + 5])
    fig.update_xaxes(range=[- 2*2*np.pi, 2*2*np.pi])

    return fig

@callback(Output("sin_equation_solution", "children"), Input("btn-decY", "n_clicks"), Input("btn-incY", "n_clicks"), Input("btn-decPhase", "n_clicks"), Input("btn-incPhase", "n_clicks"), Input("btn-decAmp", "n_clicks"), Input("btn-incAmp", "n_clicks"), Input("btn-decFreq", "n_clicks"), Input("btn-incFreq", "n_clicks"), Input("btn-decCenter", "n_clicks"), Input("btn-incCenter", "n_clicks"))
def sin_equation_solution(n_decY, n_incY, n_decPhase, n_incPhase, n_decAmp, n_incAmp, n_decFreq, n_incFreq, n_decCenter, n_incCenter):
    n_phase = 0.1 * (n_incPhase - n_decPhase)
    n_amp = 1 + (n_incAmp - n_decAmp)
    n_freq = 1 + (n_incFreq - n_decFreq)
    n_center = (n_incCenter - n_decCenter)
    y_const = n_incY - n_decY
    x_solution = (np.arcsin((y_const - n_center)/n_amp) - n_phase) / n_freq
    return f"y = {n_amp} * sin({n_freq} * x + {n_phase}) + {n_center} = {y_const} =======> x = {x_solution}"
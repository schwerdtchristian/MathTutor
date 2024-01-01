import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import numpy as np

dash.register_page(__name__)

layout = html.Div([html.H4('Sinus curve parameters visualization'), dcc.Graph(id="sin_curve"), html.P(id = "sin_parameters"), html.P(id = "sin_equation"), html.Div([html.P("Amplitude"), html.Button("-", n_clicks=0, id='btn-decAmp'), html.Button("+", n_clicks=0, id='btn-incAmp')]), html.Div([html.P("Frequency"), html.Button("- Freq", n_clicks=0, id='btn-decFreq'), html.Button("+ Freq", n_clicks=0, id='btn-incFreq')]), html.Div([html.P("Phase shift"), html.Button("-", n_clicks=0, id='btn-decPhase'), html.Button("+", n_clicks=0, id='btn-incPhase')]), html.Div([html.P("Function avarage"), html.Button("-", n_clicks=0, id='btn-decCenter'), html.Button("+", n_clicks=0, id='btn-incCenter')]), dcc.Graph(id="sin_curve_2"), html.P(id = "sin_equation_2")])


@callback(Output("sin_curve", "figure"), Input("btn-decPhase", "n_clicks"), Input("btn-incPhase", "n_clicks"), Input("btn-decAmp", "n_clicks"), Input("btn-incAmp", "n_clicks"), Input("btn-decFreq", "n_clicks"), Input("btn-incFreq", "n_clicks"), Input("btn-decCenter", "n_clicks"), Input("btn-incCenter", "n_clicks"))
def draw_sin_curve(n_decPhase, n_incPhase, n_decAmp, n_incAmp, n_decFreq, n_incFreq, n_decCenter, n_incCenter):
    n_phase = 0.1 * (n_incPhase - n_decPhase)
    n_amp = 1 + (n_incAmp - n_decAmp)
    n_freq = 1 + (n_incFreq - n_decFreq)
    n_center = (n_incCenter - n_decCenter)
    x = np.linspace(-2*np.pi, 2*np.pi, 100)
    y = n_amp * np.sin(n_freq*x + n_phase) + n_center

    trace1 = go.Scatter(
        x=x,
        y=y,
        mode='lines',
    )

    trace_data = [trace1]
    fig = go.Figure(data=trace_data)
    fig.update_layout(showlegend=False)
    fig.update_yaxes(range=[n_center - 5, n_center + 5])

    return fig

@callback(Output("sin_curve_2", "figure"), Input("btn-decPhase", "n_clicks"), Input("btn-incPhase", "n_clicks"), Input("btn-decAmp", "n_clicks"), Input("btn-incAmp", "n_clicks"), Input("btn-decFreq", "n_clicks"), Input("btn-incFreq", "n_clicks"), Input("btn-decCenter", "n_clicks"), Input("btn-incCenter", "n_clicks"))
def draw_sin_curve(n_decPhase, n_incPhase, n_decAmp, n_incAmp, n_decFreq, n_incFreq, n_decCenter, n_incCenter):
    n_phase = 0.1 * (n_incPhase - n_decPhase)
    n_amp = 1 + (n_incAmp - n_decAmp)
    n_freq = 1 + (n_incFreq - n_decFreq)
    n_center = (n_incCenter - n_decCenter)
    x = np.linspace(- 2*np.pi/n_freq, 2*np.pi/n_freq, 100)
    y = n_amp * np.sin(n_freq*x + n_phase) + n_center
    B = 1 + (n_incFreq - n_decFreq)
    C = 0.1 * (n_incPhase - n_decPhase) / B

    trace1 = go.Scatter(
        x=x,
        y=y,
        mode='lines',
    )

    trace2 = go.Scatter(
        x=[0, -C],
        y=[n_center, n_center],
    )

    trace3 = go.Scatter(
        x=[0, 2*np.pi/B],
        y=[n_amp * np.sin(n_freq*0 + n_phase) + n_center, n_amp * np.sin(n_freq*2*np.pi/B + n_phase) + n_center],
    )

    trace_data = [trace1, trace2, trace3]
    fig = go.Figure(data=trace_data)
    fig["data"][0]["name"] = "sinus functions"
    fig["data"][1]["name"] = "C = phase shift"
    fig["data"][2]["name"] = "B * T = 2*pi => B = 2*pi / T, where T is the period"
    fig.update_layout(showlegend=True)
    fig.update_yaxes(range=[n_center - 5, n_center + 5])

    return fig


@callback(Output("sin_parameters", "children"), Input("btn-decPhase", "n_clicks"), Input("btn-incPhase", "n_clicks"), Input("btn-decAmp", "n_clicks"), Input("btn-incAmp", "n_clicks"), Input("btn-decFreq", "n_clicks"), Input("btn-incFreq", "n_clicks"), Input("btn-decCenter", "n_clicks"), Input("btn-incCenter", "n_clicks"))
def area_formula(n_decPhase, n_incPhase, n_decAmp, n_incAmp, n_decFreq, n_incFreq, n_decCenter, n_incCenter):
    n_phase = 0.1 * (n_incPhase - n_decPhase)
    n_amp = 1 + (n_incAmp - n_decAmp)
    n_freq = 1 + (n_incFreq - n_decFreq)
    n_center = (n_incCenter - n_decCenter)
    return f"Phase: {n_phase} and Amplitude: {n_amp} and Frequency: {n_freq} and Center: {n_center}" 

@callback(Output("sin_equation", "children"), Input("btn-decPhase", "n_clicks"), Input("btn-incPhase", "n_clicks"), Input("btn-decAmp", "n_clicks"), Input("btn-incAmp", "n_clicks"), Input("btn-decFreq", "n_clicks"), Input("btn-incFreq", "n_clicks"), Input("btn-decCenter", "n_clicks"), Input("btn-incCenter", "n_clicks"))
def area_formula(n_decPhase, n_incPhase, n_decAmp, n_incAmp, n_decFreq, n_incFreq, n_decCenter, n_incCenter):
    n_phase = 0.1 * (n_incPhase - n_decPhase)
    n_amp = 1 + (n_incAmp - n_decAmp)
    n_freq = 1 + (n_incFreq - n_decFreq)
    n_center = (n_incCenter - n_decCenter)
    return f"y = {n_amp} * sin({n_freq} * x + {n_phase}) + {n_center}"

@callback(Output("sin_equation_2", "children"), Input("btn-decPhase", "n_clicks"), Input("btn-incPhase", "n_clicks"), Input("btn-decAmp", "n_clicks"), Input("btn-incAmp", "n_clicks"), Input("btn-decFreq", "n_clicks"), Input("btn-incFreq", "n_clicks"), Input("btn-decCenter", "n_clicks"), Input("btn-incCenter", "n_clicks"))
def area_formula(n_decPhase, n_incPhase, n_decAmp, n_incAmp, n_decFreq, n_incFreq, n_decCenter, n_incCenter):
    n_amp = 1 + (n_incAmp - n_decAmp)
    B = 1 + (n_incFreq - n_decFreq)
    C = 0.1 * (n_incPhase - n_decPhase) / B
    n_center = (n_incCenter - n_decCenter)
    return f"y = A * sin(B(x + C)) + M = {n_amp} * sin({B} * (x + {C}) + {n_center}"

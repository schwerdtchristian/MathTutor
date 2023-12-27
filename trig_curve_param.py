from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import numpy as np

app = Dash(__name__)

app.layout = html.Div([html.H4('Sinus curve parameters visualization'), dcc.Graph(id="sin_curve"), html.P(id = "area_calculations"), html.Button("Dec phase", n_clicks=0, id='btn-decPhase'), html.Button("Inc phase", n_clicks=0, id='btn-incPhase'), html.Button("Dec Amp", n_clicks=0, id='btn-decAmp'), html.Button("Inc Amp", n_clicks=0, id='btn-incAmp'), html.Button("Dec Freq", n_clicks=0, id='btn-decFreq'), html.Button("Inc Freq", n_clicks=0, id='btn-incFreq')])


@app.callback(Output("sin_curve", "figure"), Input("btn-decPhase", "n_clicks"), Input("btn-incPhase", "n_clicks"), Input("btn-decAmp", "n_clicks"), Input("btn-incAmp", "n_clicks"), Input("btn-decFreq", "n_clicks"), Input("btn-incFreq", "n_clicks"))
def draw_sin_curve(n_decPhase, n_incPhase, n_decAmp, n_incAmp, n_decFreq, n_incFreq):
    n_phase = 0.1 * (n_incPhase - n_decPhase)
    n_amp = 1 + (n_incAmp - n_decAmp)
    n_freq = 1 + (n_incFreq - n_decFreq)
    x = np.linspace(-2*np.pi, 2*np.pi, 100)
    y = n_amp * np.sin(n_freq*x + n_phase)

    trace1 = go.Scatter(
        x=x,
        y=y,
        mode='lines',
    )

    trace_data = [trace1]
    fig = go.Figure(data=trace_data)
    fig.update_layout(showlegend=False)
    fig.update_yaxes(range=[-5, 5])

    return fig


@app.callback(Output("area_calculations", "children"), Input("btn-decPhase", "n_clicks"), Input("btn-incPhase", "n_clicks"), Input("btn-decAmp", "n_clicks"), Input("btn-incAmp", "n_clicks"), Input("btn-decFreq", "n_clicks"), Input("btn-incFreq", "n_clicks"))
def area_formula(n_decPhase, n_incPhase, n_decAmp, n_incAmp, n_decFreq, n_incFreq):
    n_phase = 0.1 * (n_incPhase - n_decPhase)
    n_amp = 1 + (n_incAmp - n_decAmp)
    n_freq = 1 + (n_incFreq - n_decFreq)
    return f"Phase: {n_phase} and Amplitude: {n_amp} and Frequency: {n_freq}" 


app.run_server(debug=True)
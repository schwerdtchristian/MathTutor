import dash
from dash import dcc, html, Input, Output, ctx, callback
import plotly.graph_objects as go

dash.register_page(module=__name__, name="Percent, promille, PPM Conversion")


# -----------------------------
# Helper: Create one rectangle graph (with color coding)
# -----------------------------
def make_graph(unit, value):
    # ---- Unit settings ----
    if unit == "Percent":
        max_val = 100
        major_step = 10
        fill_fraction = value / 100
        color = "#1f77b4"   # blue

    elif unit == "Promille":
        max_val = 1000
        major_step = 100
        fill_fraction = value / 1000
        color = "#2ca02c"   # green

    else:  # PPM
        max_val = 1_000_000
        major_step = 100_000
        fill_fraction = value / 1_000_000
        color = "#ff7f0e"   # orange

    # ---- Major ticks ----
    major_ticks = list(range(0, max_val + 1, major_step))
    major_tickvals = [t / max_val for t in major_ticks]

    # ---- Minor ticks (always 9 between majors) ----
    minor_ticks = []
    for i in range(len(major_ticks) - 1):
        start = major_ticks[i]
        stop = major_ticks[i + 1]
        step = (stop - start) / 10.0
        for j in range(1, 10):   # 9 minor ticks
            minor_ticks.append(start + j * step)

    minor_tickvals = [t / max_val for t in minor_ticks]

    right_limit = max(1, fill_fraction)

    # ---- Create figure ----
    fig = go.Figure()

    # Fill area (always below ticks)
    fig.add_shape(
        type="rect",
        x0=0, y0=0,
        x1=fill_fraction, y1=1,
        fillcolor=color,
        line=dict(color=color, width=2),
        layer="below"
    )

    # Border
    fig.add_shape(
        type="rect",
        x0=0, y0=0,
        x1=1, y1=1,
        line=dict(color=color, width=3),
        fillcolor="rgba(0,0,0,0)",
        layer="below"
    )

    # ---- Axis configuration ----
    fig.update_xaxes(
        range=[0, right_limit],

        # === Major ticks ===
        tickvals=major_tickvals,
        ticktext=[str(t) for t in major_ticks],
        ticks="outside",
        ticklen=10,       # long, consistent major ticks
        tickwidth=3,      # thicker major ticks
        tickcolor="black",

        # === Minor ticks ===
        minor=dict(
            tickvals=minor_tickvals,
            ticks="outside",
            ticklen=6,    # shorter than major
            tickwidth=1,  # thin, consistent minor ticks
            tickcolor="black"
        ),

        fixedrange=True
    )

    fig.update_yaxes(
        range=[-0.3, 1],
        visible=False,
        fixedrange=True
    )

    fig.update_layout(
        title=unit,
        margin=dict(l=10, r=10, t=40, b=40),
        height=140
    )

    return fig


# -----------------------------
# Layout
# -----------------------------
layout = html.Div([
    html.H4(
        'Percent, promille and PPM Conversion',
        style={"font-size": "28px", "text-align": "center", "margin-bottom": "20px"}
    ),

    # ---- Row 1: Percent ----
    html.Div([
        html.Div([
            html.Label("Percent", style={'fontWeight': 'bold', "display": "block"}),
            dcc.Input(
                id="percent-input",
                type="number",
                value=1,
                style={"width": "120px"},
                debounce=True
            )
        ], style={"width": "200px", "padding": "10px"}),

        html.Div([
            dcc.Graph(
                id="percent-graph",
                style={"height": "140px", "width": "100%"}
            )
        ], style={"flex": "1"})
    ], style={
        "display": "flex",
        "alignItems": "center",
        "marginBottom": "15px"
    }),

    # ---- Row 2: Promille ----
    html.Div([
        html.Div([
            html.Label("Promille", style={'fontWeight': 'bold', "display": "block"}),
            dcc.Input(
                id="promille-input",
                type="number",
                value=10,
                style={"width": "120px"},
                debounce=True
            )
        ], style={"width": "200px", "padding": "10px"}),

        html.Div([
            dcc.Graph(
                id="promille-graph",
                style={"height": "140px", "width": "100%"}
            )
        ], style={"flex": "1"})
    ], style={
        "display": "flex",
        "alignItems": "center",
        "marginBottom": "15px"
    }),

    # ---- Row 3: PPM ----
    html.Div([
        html.Div([
            html.Label("Parts per million", style={'fontWeight': 'bold', "display": "block"}),
            dcc.Input(
                id="ppm-input",
                type="number",
                value=10000,
                style={"width": "120px"},
                debounce=True
            )
        ], style={"width": "200px", "padding": "10px"}),

        html.Div([
            dcc.Graph(
                id="ppm-graph",
                style={"height": "140px", "width": "100%"}
            )
        ], style={"flex": "1"})
    ], style={
        "display": "flex",
        "alignItems": "center"
    })

], style={"fontFamily": "Arial, sans-serif", "padding": "10px"})


# -----------------------------
# Callback
# -----------------------------
@callback(
    Output("percent-input", "value"),
    Output("promille-input", "value"),
    Output("ppm-input", "value"),
    Output("percent-graph", "figure"),
    Output("promille-graph", "figure"),
    Output("ppm-graph", "figure"),
    Input("percent-input", "value"),
    Input("promille-input", "value"),
    Input("ppm-input", "value")
)
def update_all(percent_val, promille_val, ppm_val):

    percent_val = percent_val or 0
    promille_val = promille_val or 0
    ppm_val = ppm_val or 0

    trigger = ctx.triggered_id

    if trigger == "percent-input":
        percent = float(percent_val)
        promille = percent * 10
        ppm = percent * 10000

    elif trigger == "promille-input":
        promille = float(promille_val)
        percent = promille / 10
        ppm = promille * 1000

    elif trigger == "ppm-input":
        ppm = float(ppm_val)
        percent = ppm / 10000
        promille = ppm / 1000

    else:  # initial load
        percent = float(percent_val)
        promille = float(promille_val)
        ppm = float(ppm_val)

    return (
        percent,
        promille,
        ppm,
        make_graph("Percent", percent),
        make_graph("Promille", promille),
        make_graph("PPM", ppm)
    )

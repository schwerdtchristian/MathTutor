import dash
from dash import dcc, html, Input, Output, ctx, callback
import plotly.graph_objects as go

dash.register_page(module=__name__, name="Percent, promille, PPM Conversion")

layout = html.Div([
    html.H1("Unit Conversion and Fill Visualization", style={'textAlign': 'center'}),

    html.Div([
        html.Div([
            html.Label("Percent", style={'fontWeight': 'bold'}),
            dcc.Input(
                id="percent-input",
                type="number",
                value=1,
                style={"width": "150px"},
                debounce=True
            )
        ], style={"marginBottom": "20px"}),

        html.Div([
            html.Label("Promille", style={'fontWeight': 'bold'}),
            dcc.Input(
                id="promille-input",
                type="number",
                value=10,
                style={"width": "150px"},
                debounce=True
            )
        ], style={"marginBottom": "20px"}),

        html.Div([
            html.Label("Parts per million", style={'fontWeight': 'bold'}),
            dcc.Input(
                id="ppm-input",
                type="number",
                value=10000,
                style={"width": "150px"},
                debounce=True
            )
        ], style={"marginBottom": "20px"})
    ], style={
        "width": "200px",
        "float": "left",
        "padding": "20px"
    }),

    html.Div([
        html.Div(
            id="unit-label",
            style={
                "textAlign": "center",
                "fontSize": "24px",
                "marginTop": "100px",
                "marginBottom": "10px",
                "fontWeight": "bold"
            }
        ),

        dcc.Graph(
            id="rectangle-graph",
            figure={},
            style={
                "height": "300px",
                "width": "80%",
                "margin": "0 auto"
            }
        )
    ], style={
        "marginLeft": "220px",
        "paddingTop": "100px"
    })
], style={"fontFamily": "Arial, sans-serif"})


@callback(
    Output("percent-input", "value"),
    Output("promille-input", "value"),
    Output("ppm-input", "value"),
    Output("rectangle-graph", "figure"),
    Output("unit-label", "children"),
    Input("percent-input", "value"),
    Input("promille-input", "value"),
    Input("ppm-input", "value")
)
def update_values(percent_val, promille_val, ppm_val):
    trigger = ctx.triggered_id

    percent_val = percent_val or 0
    promille_val = promille_val or 0
    ppm_val = ppm_val or 0

    if trigger == "percent-input":
        percent = float(percent_val)
        promille = percent * 10
        ppm = percent * 10000
        chosen = "Percent"
        max_value = 100
    elif trigger == "promille-input":
        promille = float(promille_val)
        percent = promille / 10
        ppm = promille * 1000
        chosen = "Promille"
        max_value = 1000
    elif trigger == "ppm-input":
        ppm = float(ppm_val)
        percent = ppm / 10000
        promille = ppm / 1000
        chosen = "Parts per million"
        max_value = 1_000_000
    else:
        percent = float(percent_val)
        promille = float(promille_val)
        ppm = float(ppm_val)
        chosen = "Percent"
        max_value = 100

    # Fill fraction WITHOUT CLAMPING
    if chosen == "Percent":
        fill_fraction = percent / 100
    elif chosen == "Promille":
        fill_fraction = promille / 1000
    else:
        fill_fraction = ppm / 1_000_000

    right_limit = max(1, fill_fraction)

    fig = go.Figure()
    # Add fill area first
    fig.add_shape(
        type="rect",
        x0=0,
        y0=0,
        x1=fill_fraction,
        y1=1,
        fillcolor="darkblue",
        line=dict(color="darkblue")
    )
    # Add border last
    fig.add_shape(
        type="rect",
        x0=0,
        y0=0,
        x1=1,
        y1=1,
        line=dict(color="black", width=4),
        fillcolor="rgba(0,0,0,0)"
    )

    # Determine ticks
    if chosen == "Percent":
        ticks = [i * 10 for i in range(11)]
        max_val = 100
    elif chosen == "Promille":
        ticks = [i * 100 for i in range(11)]
        max_val = 1000
    else:
        ticks = [i * 100_000 for i in range(11)]
        max_val = 1_000_000

    fig.update_layout(
        xaxis=dict(
            range=[0, right_limit],
            tickvals=[t / max_val for t in ticks],
            ticktext=[str(t) for t in ticks],
            fixedrange=True
        ),
        yaxis=dict(
            range=[-0.3, 1],
            visible=False,
            fixedrange=True
        ),
        margin=dict(l=20, r=20, t=20, b=100),
        height=350
    )

    return percent, promille, ppm, fig, chosen

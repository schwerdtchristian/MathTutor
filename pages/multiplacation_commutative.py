import dash
from dash import html, dcc, Input, Output, callback

dash.register_page(
    module=__name__,
    name="Multiplication - commutative operation"
)

layout = html.Div(
    style={"padding": "20px", "position": "relative"},
    children=[

        # Top input row
        html.Div(
            style={
                "display": "flex",
                "alignItems": "center",
                "gap": "10px",
                "marginBottom": "20px"
            },
            children=[
                dcc.Input(
                    id="input-rows",
                    type="number",
                    min=1,
                    step=1,
                    placeholder="Rows",
                    style={"width": "80px"}
                ),
                html.Div("x"),
                dcc.Input(
                    id="input-cols",
                    type="number",
                    min=1,
                    step=1,
                    placeholder="Columns",
                    style={"width": "80px"}
                ),
            ],
        ),

        # TOP grid + label
        html.Div(
            id="top-grid-row",
            style={
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "center",
                "gap": "20px",
                "marginBottom": "20px"
            }
        ),

        # Original TURN symbol (centered)
        html.Div("↻", style={
            "fontSize": "60px",
            "textAlign": "center",
            "padding": "20px"
        }),

        # BOTTOM grid + label
        html.Div(
            id="bottom-grid-row",
            style={
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "center",
                "gap": "20px",
                "marginTop": "20px"
            }
        ),

        # The => and equality text moved far to the right
        html.Div(
            style={
                "display": "flex",
                "alignItems": "center",
                "position": "absolute",
                "right": "40px",
                "top": "50%",
                "transform": "translateY(-50%)",
                "gap": "20px"
            },
            children=[
                html.Div(
                    "⇒",
                    style={"fontSize": "80px"}
                ),
                html.Div(
                    id="equality-label",
                    style={"fontSize": "28px", "fontWeight": "bold"}
                )
            ]
        )
    ]
)

# Helper function --------------------------------------------------------------

def make_grid(rows, cols, size, grid_id):
    squares = [
        html.Div(
            style={
                "width": f"{size}px",
                "height": f"{size}px",
                "backgroundColor": "blue",
                "borderRadius": "3px",
            }
        )
        for _ in range(rows * cols)
    ]

    return html.Div(
        squares,
        id=grid_id,
        style={
            "display": "grid",
            "gridTemplateRows": f"repeat({rows}, {size}px)",
            "gridTemplateColumns": f"repeat({cols}, {size}px)",
            "gap": "8px",
            "justifyContent": "center",
            "alignItems": "center",
            "overflow": "hidden",
        },
    )


# Callback --------------------------------------------------------------------

@callback(
    Output("top-grid-row", "children"),
    Output("bottom-grid-row", "children"),
    Output("equality-label", "children"),
    Input("input-rows", "value"),
    Input("input-cols", "value"),
)
def update_grids(rows, cols):

    if not rows or not cols or rows <= 0 or cols <= 0:
        return [], [], ""

    # Compute a reasonable square size
    available_width = 0.8 * 1000
    available_height = 0.8 * 800

    size_by_width = available_width / cols
    size_by_height = available_height / rows
    square_size = max(5, min(size_by_width, size_by_height, 50))

    # Create grids
    top_grid = make_grid(rows, cols, square_size, "top-grid")
    bottom_grid = make_grid(cols, rows, square_size, "bottom-grid")

    # Labels
    top_label = html.Div(
        f"{rows} × {cols}",
        style={"fontSize": "22px", "fontWeight": "bold"}
    )

    bottom_label = html.Div(
        f"{cols} × {rows}",
        style={"fontSize": "22px", "fontWeight": "bold"}
    )

    equality = f"{cols} × {rows} = {rows} × {cols}"

    return [top_grid, top_label], [bottom_grid, bottom_label], equality

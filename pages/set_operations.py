import math
import dash
from dash import html, dcc, Input, Output
import dash_svg as svg

dash.register_page(__name__, path="/set-theory", name="Set operations")

# Colors
COLOR_A = "#add8e6"     # light blue
COLOR_B = "#90ee90"     # light green
HIGHLIGHT = "#add8e6"   # highlight color for operations
NEUTRAL = "none"        # no fill when not highlighted

# Geometry (SVG coordinates)
CX_A, CY_A, R_A = 200.0, 160.0, 120.0
CX_B, CY_B, R_B = 360.0, 160.0, 120.0

# ---------- Geometry helpers to build SVG path strings ----------

def circle_path(cx, cy, r):
    """Return an SVG path string for a full circle (two arcs)."""
    # Use two half-arcs to make a full circle
    return (
        f"M {cx + r:.6f} {cy:.6f} "
        f"A {r:.6f} {r:.6f} 0 1 0 {cx - r:.6f} {cy:.6f} "
        f"A {r:.6f} {r:.6f} 0 1 0 {cx + r:.6f} {cy:.6f} Z"
    )

def intersection_points(cx0, cy0, r0, cx1, cy1, r1):
    """Return the two intersection points (x1,y1), (x2,y2) of two circles.
       If no intersection, return None."""
    dx = cx1 - cx0
    dy = cy1 - cy0
    d = math.hypot(dx, dy)
    if d <= 1e-9 or d >= (r0 + r1) or d <= abs(r0 - r1):
        # No proper intersection (too far apart or one inside the other or coincident)
        return None

    a = (r0**2 - r1**2 + d**2) / (2 * d)
    h_sq = r0**2 - a**2
    if h_sq < 0:
        h_sq = 0.0
    h = math.sqrt(h_sq)

    xm = cx0 + a * dx / d
    ym = cy0 + a * dy / d

    rx = -dy * (h / d)
    ry = dx * (h / d)

    xi1 = xm + rx
    yi1 = ym + ry
    xi2 = xm - rx
    yi2 = ym - ry
    return (xi1, yi1), (xi2, yi2)

def intersection_path(cx0, cy0, r0, cx1, cy1, r1):
    """Return an SVG path string describing the intersection region of two circles.
       Path goes: intersection pt1 -> arc on circle0 to pt2 -> arc on circle1 back -> close."""
    pts = intersection_points(cx0, cy0, r0, cx1, cy1, r1)
    if pts is None:
        return ""  # no intersection

    (x1, y1), (x2, y2) = pts

    # Arc flags:
    # We'll use the smaller arcs that form the lens.
    # For both arcs set large-arc-flag=0, and choose sweep flags so arcs go the correct direction.
    # For the arc on circle A from p1 -> p2 we choose sweepA = 0 or 1 depending on orientation.
    # A robust way: compute angles of points relative to each circle center and set sweep flags accordingly.

    def angle(cx, cy, x, y):
        return math.atan2(y - cy, x - cx)

    angA1 = angle(cx0, cy0, x1, y1)
    angA2 = angle(cx0, cy0, x2, y2)
    angB1 = angle(cx1, cy1, x1, y1)
    angB2 = angle(cx1, cy1, x2, y2)

    # Determine sweep flags so that arcs go through the lens interior.
    # We want the arc on A from p1 to p2 to go the shorter way inside the lens.
    def sweep_flag(a1, a2):
        diff = (a2 - a1) % (2 * math.pi)
        return 1 if diff > math.pi else 0

    sweepA = sweep_flag(angA1, angA2)
    sweepB = sweep_flag(angB2, angB1)  # note reversed order for B arc back to p1

    # Build path: move to p1, arc on A to p2, arc on B back to p1, close.
    path = (
        f"M {x1:.6f} {y1:.6f} "
        f"A {r0:.6f} {r0:.6f} 0 0 {sweepA} {x2:.6f} {y2:.6f} "
        f"A {r1:.6f} {r1:.6f} 0 0 {sweepB} {x1:.6f} {y1:.6f} Z"
    )
    return path

# Build base paths
CIRCLE_A_PATH = circle_path(CX_A, CY_A, R_A)
CIRCLE_B_PATH = circle_path(CX_B, CY_B, R_B)
INTERS_PATH = intersection_path(CX_A, CY_A, R_A, CX_B, CY_B, R_B)

# For A_only and B_only we draw the full circle path then also include the intersection path
# as a *subpath* and rely on fill-rule="evenodd" to subtract the intersection region.
A_ONLY_PATH = CIRCLE_A_PATH + " " + INTERS_PATH if INTERS_PATH else CIRCLE_A_PATH
B_ONLY_PATH = CIRCLE_B_PATH + " " + INTERS_PATH if INTERS_PATH else CIRCLE_B_PATH

# ---------- Layout ----------
layout = html.Div([

    html.H1("Set Operations – Venn Diagram"),

    html.Div([

        # LEFT: labels, inputs, buttons
        html.Div([

            html.Div([
                html.Label("Set A", style={"fontWeight": "bold", "color": COLOR_A}),
                dcc.Input(id="input-set-a", type="text",
                          placeholder="e.g. 1,2,3",
                          style={"width": "150px", "marginBottom": "12px"})
            ], style={"display": "flex", "flexDirection": "column", "marginBottom": "8px"}),

            html.Div([
                html.Label("Set B", style={"fontWeight": "bold", "color": COLOR_B}),
                dcc.Input(id="input-set-b", type="text",
                          placeholder="e.g. 2,3,4",
                          style={"width": "150px", "marginBottom": "20px"})
            ], style={"display": "flex", "flexDirection": "column", "marginBottom": "12px"}),

            html.Div([
                html.Button("A ∪ B", id="btn-union", n_clicks=0,
                            style={"width": "150px", "marginBottom": "8px"}),
                html.Button("A ∩ B", id="btn-intersect", n_clicks=0,
                            style={"width": "150px", "marginBottom": "8px"}),
                html.Button("A", id="btn-A-only", n_clicks=0,
                            style={"width": "150px", "marginBottom": "8px"}),
                html.Button("B", id="btn-B-only", n_clicks=0,
                            style={"width": "150px", "marginBottom": "8px"}),
                html.Button("A - B", id="btn-A-minus-B", n_clicks=0,
                            style={"width": "150px", "marginBottom": "8px"}),
                html.Button("B - A", id="btn-B-minus-A", n_clicks=0,
                            style={"width": "150px", "marginBottom": "8px"}),
                html.Button("A Δ B", id="btn-A-delta-B", n_clicks=0,
                            style={"width": "150px"})
            ], style={"display": "flex", "flexDirection": "column", "marginTop": "12px"})
        ], style={"marginRight": "80px", "minWidth": "200px"}),

        # RIGHT: Venn diagram
        html.Div([
            svg.Svg([
                # Circle outlines (no fill)
                svg.Circle(cx=str(CX_A), cy=str(CY_A), r=str(R_A),
                           fill="none", stroke=COLOR_A, strokeWidth="4"),
                svg.Circle(cx=str(CX_B), cy=str(CY_B), r=str(R_B),
                           fill="none", stroke=COLOR_B, strokeWidth="4"),

                # A only region path (fill-rule="evenodd" subtracts intersection)
                svg.Path(
                    id="path-A-only",
                    d=A_ONLY_PATH,
                    fill="none",
                    fillRule="evenodd",
                    stroke="none"
                ),

                # B only region path
                svg.Path(
                    id="path-B-only",
                    d=B_ONLY_PATH,
                    fill="none",
                    fillRule="evenodd",
                    stroke="none"
                ),

                # Intersection region path
                svg.Path(
                    id="path-intersection",
                    d=INTERS_PATH,
                    fill="none",
                    stroke="none"
                ),

                # Text positions for the three regions
                svg.Text(id="A_only", x=str(CX_A - 40), y=str(CY_A),
                         fontSize="20", textAnchor="middle", fill="black"),
                svg.Text(id="B_only", x=str(CX_B + 40), y=str(CY_B),
                         fontSize="20", textAnchor="middle", fill="black"),
                svg.Text(id="A_and_B", x=str((CX_A + CX_B)/2), y=str(CY_A),
                         fontSize="20", textAnchor="middle", fill="black"),
            ],
            width="700", height="380", style={"border": "1px solid #999"})
        ], style={"marginLeft": "120px"})
    ],
    style={"display": "flex", "flexDirection": "row", "alignItems": "flex-start",
           "marginTop": "20px"})
])


# ---------- Callbacks ----------

# Update textual lists in regions
@dash.callback(
    Output("A_only", "children"),
    Output("B_only", "children"),
    Output("A_and_B", "children"),
    Input("input-set-a", "value"),
    Input("input-set-b", "value"),
)
def update_text(a_values, b_values):
    def parse_numbers(text):
        if not text:
            return set()
        parts = [p.strip() for p in text.split(",")]
        return {p for p in parts if p.isdigit()}

    setA = parse_numbers(a_values)
    setB = parse_numbers(b_values)

    onlyA = sorted(setA - setB)
    onlyB = sorted(setB - setA)
    both = sorted(setA & setB)
    return ", ".join(onlyA), ", ".join(onlyB), ", ".join(both)


# Update fill colors for the three disjoint regions (A_only, B_only, intersection)
@dash.callback(
    Output("path-A-only", "fill"),
    Output("path-B-only", "fill"),
    Output("path-intersection", "fill"),
    Output("path-A-only", "fillOpacity"),
    Output("path-B-only", "fillOpacity"),
    Output("path-intersection", "fillOpacity"),
    Input("btn-union", "n_clicks"),
    Input("btn-intersect", "n_clicks"),
    Input("btn-A-only", "n_clicks"),
    Input("btn-B-only", "n_clicks"),
    Input("btn-A-minus-B", "n_clicks"),
    Input("btn-B-minus-A", "n_clicks"),
    Input("btn-A-delta-B", "n_clicks")
)
def update_highlight(n_union, n_intersect, n_Aonly, n_Bonly, n_AminusB, n_BminusA, n_AdeltaB):
    ctx = dash.callback_context
    # default: all invisible
    fillA = NEUTRAL
    fillB = NEUTRAL
    fillAB = NEUTRAL
    opaA = "0"
    opaB = "0"
    opaAB = "0"

    if not ctx.triggered:
        return fillA, fillB, fillAB, opaA, opaB, opaAB

    btn = ctx.triggered[0]["prop_id"].split(".")[0]

    if btn == "btn-union":
        # highlight whole union: fill all three disjoint regions with same color
        fillA = HIGHLIGHT
        fillB = HIGHLIGHT
        fillAB = HIGHLIGHT
        opaA = opaB = opaAB = "1.0"
        return fillA, fillB, fillAB, opaA, opaB, opaAB

    if btn == "btn-intersect":
        # only intersection
        fillAB = HIGHLIGHT
        opaAB = "1.0"
        return fillA, fillB, fillAB, opaA, opaB, opaAB

    if btn == "btn-A-minus-B":
        # A minus B (A-only region)
        fillA = HIGHLIGHT
        opaA = "1.0"
        return fillA, fillB, fillAB, opaA, opaB, opaAB

    if btn == "btn-B-minus-A":
        # B minus A (B-only region)
        fillB = HIGHLIGHT
        opaB = "1.0"
        return fillA, fillB, fillAB, opaA, opaB, opaAB
    
    if btn == "btn-A-only":
        # A (Whole A region)
        fillA = HIGHLIGHT
        fillAB = HIGHLIGHT
        opaA = opaAB = "1.0"
        return fillA, fillB, fillAB, opaA, opaB, opaAB
    
    if btn == "btn-B-only":
        # A (Whole B region)
        fillB = HIGHLIGHT
        fillAB = HIGHLIGHT
        opaB = opaAB =  "1.0"
        return fillA, fillB, fillAB, opaA, opaB, opaAB
    
    if btn == "btn-A-delta-B":
        # A delta B (A and B but not intersection)
        fillB = HIGHLIGHT
        fillA = HIGHLIGHT
        opaB = opaA =  "1.0"
        return fillA, fillB, fillAB, opaA, opaB, opaAB

    return fillA, fillB, fillAB, opaA, opaB, opaAB

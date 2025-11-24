import numpy as np
import dash
from dash import html, dcc, Input, Output
import plotly.graph_objects as go

dash.register_page(__name__, path="/triangle-sum")

ANGLE_COLORS = {
    "A": "rgba(255,0,0,0.6)",
    "B": "rgba(0,200,0,0.6)",
    "C": "rgba(255,150,0,0.6)",
}

# ---------- Geometry helpers ----------

def make_angle_arc(vertex, v1, v2, radius=0.08, steps=40, inside=True):
    v1_u = v1 / np.linalg.norm(v1)
    v2_u = v2 / np.linalg.norm(v2)
    angle = np.arccos(np.clip(np.dot(v1_u, v2_u), -1, 1))
    rot = np.array([[0, -1], [1, 0]])
    perp = rot @ v1_u
    if inside:
        if np.dot(perp, v2_u) < 0:
            perp = -perp
    else:
        if np.dot(perp, v2_u) > 0:
            perp = -perp
    arc_x, arc_y = [], []
    for t in np.linspace(0, angle, steps):
        p = vertex + radius*(np.cos(t)*v1_u + np.sin(t)*perp)
        arc_x.append(p[0]); arc_y.append(p[1])
    return np.array(arc_x), np.array(arc_y)


def make_outer_arc(vertex, v1, v2, outward_dir, radius=0.12, steps=40):
    v1_u = v1 / np.linalg.norm(v1)
    v2_u = v2 / np.linalg.norm(v2)
    rot = np.array([[0, -1],[1,0]])
    perp = rot @ v1_u
    if np.dot(perp, outward_dir) < 0:
        perp = -perp
    angle = np.arccos(np.clip(np.dot(v1_u, v2_u), -1, 1))
    arc_x, arc_y = [], []
    for t in np.linspace(0, angle, steps):
        p = vertex + radius*(np.cos(t)*v1_u + np.sin(t)*perp)
        arc_x.append(p[0]); arc_y.append(p[1])
    return np.array(arc_x), np.array(arc_y)


def triangle_vertices(a_deg, b_deg):
    c_deg = 180 - a_deg - b_deg
    if c_deg <= 0:
        return None, c_deg
    A = np.radians(a_deg)
    B = np.radians(b_deg)
    C = np.radians(c_deg)
    A_pt = np.array([0.0,0.0])
    B_pt = np.array([1.0,0.0])
    a_len = np.sin(A)/np.sin(C)
    C_pt = np.array([a_len*np.cos(A), a_len*np.sin(A)])
    return np.array([A_pt,B_pt,C_pt]), c_deg


def compute_extensions(pts):
    extensions=[]
    extend_len=0.3
    centroid=np.mean(pts,axis=0)
    for i in range(3):
        vertex=pts[i]
        prev=pts[(i-1)%3]
        direction=prev-vertex
        unit=direction/np.linalg.norm(direction)
        if np.linalg.norm(vertex+0.1*unit-centroid)<np.linalg.norm(vertex-centroid):
            unit=-unit
        extensions.append((vertex, vertex+extend_len*unit))
    return extensions


# ---------- Figure builder ----------

def make_triangle_figure(pts, outer_A, outer_B, outer_C):
    # --- positions for layout ---
    triangle_shift_x = -2.0  # move triangle further left
    circle_center_x = 0.0    # circle in middle
    eq_text_x = 1.5          # equations on right

    x = pts[:,0] + triangle_shift_x
    y = pts[:,1]

    extensions = compute_extensions(pts)
    fig = go.Figure()

    # triangle edges
    fig.add_trace(go.Scatter(
        x=np.append(x,x[0]), y=np.append(y,y[0]),
        mode="lines+markers",
        marker=dict(size=10,color="blue"),
        line=dict(color="blue",width=3),
        showlegend=False
    ))

    # dashed extensions
    for i, (p1_orig, p2_orig) in enumerate(extensions):
        p1 = p1_orig + np.array([triangle_shift_x,0])
        p2 = p2_orig + np.array([triangle_shift_x,0])
        fig.add_trace(go.Scatter(
            x=[p1[0],p2[0]], y=[p1[1],p2[1]],
            mode="lines", line=dict(color="gray",dash="dash",width=2),
            showlegend=False
        ))

    # inner + outer angles
    for i,letter in enumerate(["A","B","C"]):
        vertex = np.array([x[i], y[i]])
        prev = np.array([x[(i-1)%3], y[(i-1)%3]])
        nxt = np.array([x[(i+1)%3], y[(i+1)%3]])

        v1 = prev - vertex
        v2 = nxt - vertex

        # inner arc
        ax, ay = make_angle_arc(vertex, v1, v2)
        fig.add_trace(go.Scatter(
            x=[vertex[0]]+list(ax)+[vertex[0]],
            y=[vertex[1]]+list(ay)+[vertex[1]],
            fill="toself",
            fillcolor="rgba(100,150,255,0.3)",
            line=dict(color="rgba(0,0,0,0)"),
            showlegend=False
        ))

        # inner label
        bisector = v1/np.linalg.norm(v1)+v2/np.linalg.norm(v2)
        bisector /= np.linalg.norm(bisector)
        pos = vertex + 0.06*bisector
        fig.add_annotation(x=pos[0], y=pos[1], text=chr(ord("a")+i),
                           showarrow=False, font=dict(size=18,color="blue"))

        # outer arc
        outer_bis = (-v1/np.linalg.norm(v1)+v2/np.linalg.norm(v2))
        outer_bis /= np.linalg.norm(outer_bis)
        label_pos = vertex + 0.18*outer_bis
        outward_dir = label_pos - vertex

        ov1 = v2 if i==0 else -v1
        ov2 = -v1 if i==0 else v2
        ax2, ay2 = make_outer_arc(vertex, ov1, ov2, outward_dir)
        fig.add_trace(go.Scatter(
            x=[vertex[0]]+list(ax2)+[vertex[0]],
            y=[vertex[1]]+list(ay2)+[vertex[1]],
            fill="toself",
            fillcolor=ANGLE_COLORS[letter],
            line=dict(color="rgba(0,0,0,0)"),
            showlegend=False
        ))

        # outer label
        fig.add_annotation(x=label_pos[0], y=label_pos[1],
                           text=letter, showarrow=False,
                           font=dict(size=18,color=ANGLE_COLORS[letter].replace("0.6","1")))

    # autoscale for triangle
    xmin, xmax = np.min(x), np.max(x)
    ymin, ymax = np.min(y), np.max(y)
    pad = max(xmax-xmin, ymax-ymin)*0.8
    fig.update_layout(
        margin=dict(l=20,r=20,t=20,b=20),
        xaxis=dict(range=[-2.5,2.5], scaleanchor="y", showgrid=False, visible=False),
        yaxis=dict(range=[np.mean(y)-pad, np.mean(y)+pad], showgrid=False, visible=False),
        height=600
    )

               # --- Dynamic circle with geometry-computed rotation (Option B) ---
    outer_angles = {"A": outer_A, "B": outer_B, "C": outer_C}
    center_x, center_y = circle_center_x, np.mean(y)
    radius = 0.33

    # --- Get triangle vertex positions (already shifted) ---
    vertex_labels = ["A", "B", "C"]
    vertices = [np.array([x[i], y[i]]) for i in range(3)]
    prev_pts  = [np.array([x[(i-1)%3], y[(i-1)%3]]) for i in range(3)]
    next_pts  = [np.array([x[(i+1)%3], y[(i+1)%3]]) for i in range(3)]

    # --- Compute OUTER bisector directions (absolute angles, radians) ---
    outer_dirs = {}
    for i, label in enumerate(vertex_labels):
        V = vertices[i]
        P = prev_pts[i]
        N = next_pts[i]

        v1 = P - V
        v2 = N - V
        v1_u = v1 / np.linalg.norm(v1)
        v2_u = v2 / np.linalg.norm(v2)

        # Outer bisector used in your diagram: reverse v1 then bisect
        outer_bis = -v1_u + v2_u
        outer_bis /= np.linalg.norm(outer_bis)
        outer_dirs[label] = np.arctan2(outer_bis[1], outer_bis[0])

    # --- Compute the rotation (in radians) that best aligns circle-sector midpoints
    #     with the outer_dirs. Use circular mean of per-sector required rotations. ---
    required_rots = []
    running_angle_deg = 0.0
    for label in ["A", "B", "C"]:
        span = outer_angles[label]  # degrees
        mid_deg = running_angle_deg + span / 2.0
        mid_rad = np.radians(mid_deg)  # where the sector midpoint sits if rotation = 0
        desired = outer_dirs[label]    # absolute direction we want the midpoint to point to
        # rotation required for this label:
        required_rots.append(desired - mid_rad)
        running_angle_deg += span

    # Circular average of required_rots:
    rc = np.mean(np.cos(required_rots))
    rs = np.mean(np.sin(required_rots))
    rot = np.arctan2(rs, rc)  # final rotation (radians) to apply (positive = CCW)

    # --- Draw sectors using computed rot ---
    running_angle_deg = 0.0
    for label in ["A", "B", "C"]:
        span = outer_angles[label]
        start = np.radians(running_angle_deg) + rot
        end   = np.radians(running_angle_deg + span) + rot
        theta = np.linspace(start, end, 120)

        # Filled wedge
        wedge_x = [center_x] + list(center_x + radius * np.cos(theta)) + [center_x]
        wedge_y = [center_y] + list(center_y + radius * np.sin(theta)) + [center_y]
        fig.add_trace(go.Scatter(
            x=wedge_x, y=wedge_y,
            fill="toself", fillcolor=ANGLE_COLORS[label],
            line=dict(color="black", width=1), showlegend=False
        ))

        # Radial division lines
        xs1 = center_x + radius * np.cos(start)
        ys1 = center_y + radius * np.sin(start)
        xe1 = center_x + radius * np.cos(end)
        ye1 = center_y + radius * np.sin(end)
        fig.add_trace(go.Scatter(x=[center_x, xs1], y=[center_y, ys1],
                                 mode="lines", line=dict(color="black", width=2), showlegend=False))
        fig.add_trace(go.Scatter(x=[center_x, xe1], y=[center_y, ye1],
                                 mode="lines", line=dict(color="black", width=2), showlegend=False))

        # Label just outside the wedge midpoint
        mid = (start + end) / 2.0
        fig.add_annotation(
            x=center_x + 0.48 * np.cos(mid),
            y=center_y + 0.48 * np.sin(mid),
            text=f"{label} ({span:.1f}°)",
            showarrow=False,
            font=dict(size=16, color=ANGLE_COLORS[label].replace("0.6", "1"))
        )

        running_angle_deg += span


        # equations on right
    text_x = eq_text_x
    text_y = np.mean(y)
    eq_text = (
        "Adding eq. (1), (2) and (3) ⇒ A + B + C + a + b + c = 180 + 180 + 180<br>"
        "simplifying with eq (4) ⇒ a + b + c = 180"
    )
    fig.add_annotation(
        x=text_x, y=text_y,
        text=eq_text,
        showarrow=False, font=dict(size=14), align="left"
    )

    # --- Equations under the triangle ---
    # Compute bottom of triangle
    ymin_tri = np.min(y)
    # Offset below triangle
    offset = 0.3
    eq_x = np.mean(x)  # center under triangle
    eq_y = ymin_tri - offset

    eq_text = (
        "(1) A + a = 180<br>"
        "(2) B + b = 180<br>"
        "(3) C + c = 180"
    )
    fig.add_annotation(
        x=eq_x,
        y=eq_y,
        text=eq_text,
        showarrow=False,
        font=dict(size=16, color="black"),
        xanchor="center",
        align="center"
    )

    # Dynamic sum label below the circle
    # We compute the bottom of the circle dynamically using radius
    circle_bottom = center_y - radius  # circle center minus radius
    offset = 0.3

    fig.add_annotation(
        x=center_x,
        y=circle_bottom - offset,
        text="(4) A + B + C = 360°<br>" \
        "Imagine walking around the triangle.<br>" \
        "When reaching where you started,<br>" \
        "you have turned 360°",
        showarrow=False,
        font=dict(size=18, color="black"),
        xanchor="center"
    )

    return fig


# ---------- Dash UI ----------

layout = html.Div([
    html.H4('Triangle angels sum to 180', style={"font-size": "30px", "text-align": "center"}),

    html.Div([
        html.Label("Angle a (°):"),
        dcc.Slider(id="angle-a",min=20,max=130,step=1,value=60,
                   marks={i:str(i) for i in range(20,131,10)}),
        html.Br(),
        html.Label("Angle b (°):"),
        dcc.Slider(id="angle-b",min=20,max=130,step=1,value=70,
                   marks={i:str(i) for i in range(20,131,10)}),
        html.Br(),
    ],style={"width":"80%","margin":"auto"}),

    dcc.Graph(id="triangle-graph",style={"height":"80vh"})
])


# ---------- Callbacks ----------

@dash.callback(
    Output("triangle-graph","figure"),
    Input("angle-a","value"),
    Input("angle-b","value"),
)
def update_triangle(a_deg,b_deg):
    pts, c_deg = triangle_vertices(a_deg,b_deg)
    if pts is None:
        return go.Figure()
    outer_A = 180 - a_deg
    outer_B = 180 - b_deg
    outer_C = 180 - c_deg
    fig = make_triangle_figure(pts, outer_A, outer_B, outer_C)
    return fig

import dash
from dash import Dash, html, dcc, Input, Output

app = Dash(__name__, use_pages=True)
server = app.server

app.layout = html.Div([

    # ---------- Search box ----------
    html.Div(
        dcc.Input(
            id="search-pages",
            type="text",
            placeholder="Search pages...",
            style={"width": "300px", "marginBottom": "20px"}
        ),
        style={"textAlign": "left", "margin": "20px"}
    ),

    # ---------- LINKS + IMAGE SIDE BY SIDE ----------
    html.Div([

        # --- Left: page links WITH SCROLLBAR ---
        html.Div(
            id="page-links-container",
            style={
                "width": "300px",
                "marginRight": "40px",
                "height": "220px",         # <<< NEW — slightly shorter list area
                "overflowY": "scroll",     # <<< NEW — forces vertical scrollbar
                "border": "1px solid #ccc",
                "padding": "10px"
            }
        ),

        # --- Left image ---
        html.Div([
            html.Img(
                src="/assets/Math_tutor_app_3.png",
                style={'width': '500px'}
            )
        ]),

        # --- Right image ---
        html.Div([
            html.Img(
                src="/assets/Math_tutor_app_3_flipped.png",
                style={'width': '500px'}
            )
        ]),
    ],
    style={
        "display": "flex",
        "flexDirection": "row",
        "alignItems": "flex-start",
        "justifyContent": "flex-start",
        "margin": "20px"
    }),

    # ---------- Page content below ----------
    html.Div(
        dash.page_container,
        style={"marginTop": "40px"}
    )
])


@app.callback(
    Output("page-links-container", "children"),
    Input("search-pages", "value")
)
def filter_pages(search_value):
    search_value = (search_value or "").lower()
    links = []

    for page in dash.page_registry.values():
        if search_value in page["name"].lower():
            links.append(
                html.Div(
                    dcc.Link(page["name"], href=page["path"]),
                    style={"marginBottom": "8px"}
                )
            )

    return links


if __name__ == '__main__':
    app.run(debug=True)

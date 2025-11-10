import dash
from dash import Dash, html, dcc, Input, Output

app = Dash(__name__, use_pages=True)
server = app.server

app.layout = html.Div([
    html.H1("Math tutor app"),

    # Search input
    dcc.Input(
        id="search-pages",
        type="text",
        placeholder="Search pages...",
        style={"width": "300px", "marginBottom": "20px"}
    ),

    # Container for page links
    html.Div(id="page-links-container"),

    # Page content
    dash.page_container
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
                html.Div(dcc.Link(page["name"], href=page["path"]), style={"marginBottom": "5px"})
            )
    return links


if __name__ == '__main__':
    app.run(debug=True)
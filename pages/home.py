import dash
from dash import html

dash.register_page(__name__, path='/')

layout = html.Div([
    html.H1('Welcome to this interactive math web application'),
    html.Div('Please select an area of interest above to explore this math concept further'),
])
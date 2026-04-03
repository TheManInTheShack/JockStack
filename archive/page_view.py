# ==============================================================================
# View page
# This is where we want to have a portal to various visualizations of the data
# ==============================================================================
from dash import dcc, html
import dash_bootstrap_components as dbc
from app import app
from dash_tools import *

# ==============================================================================
# Init
# ==============================================================================
print("...loading view page...")

def layout_view(init):
    # --------------------------------------------------------------------------
    # 
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Compile components
    # --------------------------------------------------------------------------
    components = []
    components.append(get_navbar(init['pages'], init['title']))
    components.append(html.P("Hello view"))
    components.append(get_footnote(init['footnote']))

    # --------------------------------------------------------------------------
    # Write out the top Level
    # --------------------------------------------------------------------------
    layout_view = html.Div(components, style=init['style_default'])
    return layout_view


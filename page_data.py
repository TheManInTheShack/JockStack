# ==============================================================================
# Data page
# By default, this is where we want to have a portal to tabular views of data
# ==============================================================================
from dash import dcc, html
import dash_bootstrap_components as dbc
from app import app
from dash_tools import *

# ==============================================================================
# Init
# ==============================================================================
print("...loading data page...")

def layout_data(init):
    # --------------------------------------------------------------------------
    # 
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Compile components
    # --------------------------------------------------------------------------
    components = []
    components.append(get_navbar(init['pages'], init['title']))
    components.append(html.P("Hello data"))
    components.append(get_footnote(init['footnote']))

    # --------------------------------------------------------------------------
    # Write out the top Level
    # --------------------------------------------------------------------------
    layout_data = html.Div(components, style=init['style_default'])
    return layout_data


# ==================================================================================================
# INDEX
# This file runs the overall dashboard program
# - Includes the other pieces as imports
# - Puts together the multi-page index and routing
# - Runs the server
# ==================================================================================================
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from app import app
from initialize import init_dict

# ==================================================================================================
# CONFIGURATION - ONLY CHANGE THIS!
# - application title
# - one import for each page
# - dictionary contains page information
# ==================================================================================================
app.title = "JockStack"

from page_start import *
from page_data import *
from page_view import *

pages = {}
pages['start']  = {'href':"/"     , 'name':"Home"  , 'func':layout_start }
pages['data']   = {'href':"/data" , 'name':"Data"  , 'func':layout_data  }
pages['view']   = {'href':"/view" , 'name':"View"  , 'func':layout_view  }

# ==================================================================================================
# Put together the multi-page index and routing
# ==================================================================================================
# ------------------------------------------------------------------------------
# Store page into the dict to be pushed into the layout
# ------------------------------------------------------------------------------
init_dict['pages'] = pages

# ------------------------------------------------------------------------------
# Single-level layout holds the whole page contents, and a storage layer holds
# data that needs to persist between pages
# ------------------------------------------------------------------------------
app_components = []
app_components.append(dcc.Location(id='url', refresh=False))
app_components.append(html.Div(id='page-content'))
app_components.append(html.Div(id='data_storage'))

app.layout = dbc.Container(app_components, fluid=True)

# ------------------------------------------------------------------------------
# Path routing via a special callback
# - The output is the Div that we made just above
# - The input is the url typed into the browser
# - Each formal path ending will have a corresponding function in layouts
# ------------------------------------------------------------------------------
@app.callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    for page in pages:
        if pathname == pages[page]['href']:
            out = pages[page]['func'](init_dict)
            return out
    return '404'

# ==================================================================================================
# Run the server
# ==================================================================================================
# ------------------------------------------------------------------------------
# if in production mode we need to have a reference to the server for wsgi
# ------------------------------------------------------------------------------
server = app.server

# ------------------------------------------------------------------------------
# If we are running it in test mode
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    print("...starting server...")
    app.run_server(debug=True)

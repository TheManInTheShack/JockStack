# ==============================================================================
# Start page
# ==============================================================================
from dash import dcc, html, Input, Output, State, ctx
import dash_bootstrap_components as dbc
from app import app
from dash_tools import *
import jockstack
import json

# ==============================================================================
# Layout function
# ==============================================================================
print("...loading starting page...")
def layout_start(init):
    # --------------------------------------------------------------------------
    # Navigation and footnote are standard
    # --------------------------------------------------------------------------
    navbar = get_navbar(init['pages'], init['title'])
    footnote = get_footnote(init['footnote'])

    # --------------------------------------------------------------------------
    # Set up control component to trigger events
    # --------------------------------------------------------------------------
    controls = []
    controls.append(dcc.Input(id="numjocks", value="0", type='number'))
    controls.append(dbc.Button("Begin New Stack", id="newstack-button", className="me-2", n_clicks=0))
    controls.append(dbc.Button("Hi, new Jock!",   id="newjock-button",  className="me-2", n_clicks=0))

    control_panel = html.Div(controls)

    # --------------------------------------------------------------------------
    # Set up storage variables for persistent data
    # --------------------------------------------------------------------------
    storedata = []
    storedata.append(dcc.Store(id='jockstack', storage_type="session"))

    storage = html.Div(storedata)

    # --------------------------------------------------------------------------
    # Compile all components and return the top level
    # --------------------------------------------------------------------------
    components = []
    components.append(navbar)
    components.append(control_panel)
    components.append(html.Span(id="output_viewport"))
    components.append(footnote)
    components.append(storage)

    layout = html.Div(components, style=init['style_default'])
    return layout


# ==============================================================================
# Callback functions
# ==============================================================================

# ------------------------------------------------------------------------------
# When the button is pushed, generate a new stack in full, and store it
# ------------------------------------------------------------------------------
@app.callback([Output("jockstack","data"),Output("newjock-button","n_clicks")], [Input("newstack-button","n_clicks"), Input("numjocks","value")])
def generate_new_stack(newstack_n, numjocks):
    trig = ctx.triggered_id if not None else None
    if (not trig) or (trig == "newstack-button"):
        if not numjocks:
            numjocks = 0
        numjocks = int(numjocks)
        if numjocks > 1000:
            numjocks = 1000
        jocks = jockstack.stack_jocks(numjocks)
        return [json.dumps(jocks), 0]
    else:
        return dash.no_update


# ------------------------------------------------------------------------------
# Build the output text, based on the stack and the current number that have
# been revealed
# ------------------------------------------------------------------------------
@app.callback([Output("output_viewport","children")], [Input("newjock-button","n_clicks"),Input("jockstack","data")] )
def introduce_new_jock(newjock_n, jockstack_data):
    # --------------------------------------------------------------------------
    # Unpack
    # --------------------------------------------------------------------------
    trig = ctx.triggered_id if not None else None
    jocks = json.loads(jockstack_data)
    totaljocks = len(jocks)

    # --------------------------------------------------------------------------
    # Write out the full text
    # --------------------------------------------------------------------------
    stack = []
    if totaljocks == 0:
        stack.append("T'ere be no Jocks at this time!")
    else:
        stack.append(f"T'ere are to be {totaljocks} Jocks this time!")
        stack.append(f"new Jocks: {newjock_n}")
        stack.append("")
        for i, jock in enumerate(jocks):
            if (i+1) > newjock_n:
                break
            stack.append(f"Oi! We be {jocks[jock]}")
            stack.append("")
        stack.append("")
        stack.append("...and tha's all the Jocks t'ere are!")

    if newjock_n > totaljocks:
        stack.append("No more Jocks!")

    # --------------------------------------------------------------------------
    # Format and return
    # --------------------------------------------------------------------------
    text = "\n".join(stack)
    md = dcc.Markdown(children=text)
    return [md]


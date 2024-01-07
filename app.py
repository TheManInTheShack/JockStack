# ==============================================================================
# This control structure is pulled in from the index; it is separated to avoid 
# a circular reference. It is just instantiating the overall application.
#
# I think this could be made better by removing the stylesheet reference here,
# but I don't know enough about how those work yet.  Revisit this later.
# ==============================================================================
import dash
import dash_bootstrap_components as dbc
app = dash.Dash(__name__, suppress_callback_exceptions=True,update_title="Loading...", external_stylesheets=[dbc.themes.BOOTSTRAP])

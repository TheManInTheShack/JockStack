# ==================================================================================================
# Imports
# ==================================================================================================
import sys
import os
import json

# ==================================================================================================
# Initialize
# ==================================================================================================
# ------------------------------------------------------------------------------
# Start
# ------------------------------------------------------------------------------
print("-"*80)
print("Starting...")
print("-"*80)

# ------------------------------------------------------------------------------
# Put together the blocks of text and image assets used in all sheets
# ------------------------------------------------------------------------------
title = "JockStack"

footnote = {}
footnote['credits'] = "Feegles are an invention of Sir Terry Pratchett, who would hopefully approve of this silly-but-slightly-profound endeavor. Application implementation by Grant Dickerson, copyright 2023."
footnote['revnum']  = "Rev.0"

# ==================================================================================================
# Store default style components
# ==================================================================================================
# ------------------------------------------------------------------------------
# Default
# ------------------------------------------------------------------------------
style_default = {}
style_default['backgroundColor']  = '#111111'
style_default['color']            = '#FFFFFF'
style_default['textAlign']        = 'center'

# ==================================================================================================
# Pull in the main data source shared by all pages
# ==================================================================================================
# ------------------------------------------------------------------------------
# Read any external data files into memory
# ------------------------------------------------------------------------------
print("...reading data...")
data = {}

# ------------------------------------------------------------------------------
# Derive any universal metrics
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Hold all the initialized data so we can pass it to the pages
# ------------------------------------------------------------------------------
init_dict = {}
init_dict['title']             = title
init_dict['footnote']          = footnote
init_dict['style_default']     = style_default
init_dict['data']              = data


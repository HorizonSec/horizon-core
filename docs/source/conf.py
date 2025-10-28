# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
import os
project = 'Horizon Core'
copyright = '2025, HorizonSec Team'
author = 'HorizonSec Team'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',      # Include documentation from docstrings
    'sphinx.ext.viewcode',     # Add links to highlighted source code
    'sphinx.ext.napoleon',     # Support for NumPy and Google style docstrings
    'sphinx.ext.githubpages',  # Publish HTML docs in GitHub Pages
    'myst_parser',             # Support for Markdown files
]

templates_path = ['_templates']
exclude_patterns = ['']

# -- Options for HTML output ------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']

# -- Extension configuration -------------------------------------------------

# Napoleon settings for Google/NumPy style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_type_aliases = None

# Autodoc settings
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}

# MyST parser settings
myst_enable_extensions = [
    "deflist",
    "tasklist",
    "colon_fence",
]

# -- Path setup --------------------------------------------------------------

sys.path.insert(0, os.path.abspath('../../'))

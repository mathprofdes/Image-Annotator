# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
from __future__ import annotations

import importlib.util
import os
import sys
import time
import datetime

from sphinx.application import Sphinx

project = 'Image Annotator User\'s Guide'
copyright = '2026, Don Spickler'
author = 'Don Spickler'
#release = '1.1.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.mathjax"
]

templates_path = ['_templates']
html_static_path = ['_static']
html_css_files = ["custom.css"]
html_last_updated_fmt = '%A, %B %d, %Y  -  %I:%M %p'
exclude_patterns = []
master_doc = 'index'

mathjax_path="es5/tex-chtml.js"

# -- Options for LaTeX output --------------------------------------------------

latex_documents = [
  ('index', 'Image_Annotator_Users_Guide.tex', 'Image Annotator User\'s Guide',
   'Don Spickler', 'manual', True),
]

latex_elements = {
    'figure_align' : 'H'
}

#latex_toplevel_sectioning = 'chapter'

# -- Options for HTML output -------------------------------------------------

html_logo = os.path.join("Images", "ImageAnnIcon.png")
html_theme = 'pydata_sphinx_theme'
html_show_sourcelink = False
html_show_sphinx = True

html_theme_options = {
    "collapse_navigation": True,
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/mathprofdes/",
            "icon": "fa-brands fa-square-github",
            "type": "fontawesome",
        }
    ],
#    "navbar_end": ["theme-switcher", "navbar-icon-links"],
    "navbar_persistent": [], 
    "search_bar_text": "Search...",
    "navbar_end": ["search-field.html", "navbar-icon-links"],
    "footer_start": ["copyright", "last-updated"],
    "footer_end": ["sphinx-version", "theme-version"],
    "navigation_depth": 5,
    "navigation_with_keys": True,
    "secondary_sidebar_items": ["page-toc"],
    "show_toc_level": 5,
    "show_nav_level": 5,
    "use_edit_page_button": False,

    "navbar_align": "left",
    #"primary_sidebar_end": [],
    # "primary_sidebar_end": ["indices.html"],
    "back_to_top_button": False,
    "header_links_before_dropdown": 7
}

html_sidebars = {
    "*": []
}


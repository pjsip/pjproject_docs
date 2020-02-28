# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import subprocess

# sys.path.insert(0, os.path.abspath('.'))

#sys.path.append( "/home/me/docproj/ext/breathe/" )

# -- Run doxygen and stuff if were in RTD ------------------------------------
is_in_rtd = os.environ.get('READTHEDOCS', None) == 'True'

if is_in_rtd:
    if os.path.exists('source/'):
        os.chdir('source')
    
    for doxy_dir in ['pjlib', 'pjlib-util', 'pjnath', 'pjmedia', 'pjsip']:
        cmd = f'cd pjproject{os.sep}{doxy_dir} && doxygen docs{os.sep}doxygen.cfg'
        print(f'==> {cmd}')
        rc = subprocess.call(cmd, shell=True)
        if rc:
            sys.exit(rc)
            
        api_dir = 'pjlib_util' if doxy_dir=='pjlib-util' else doxy_dir
        cmd = f'breathe-apidoc -f -p {api_dir} ' \
              f'-o api{os.sep}generated{os.sep}{api_dir} ' \
              f'pjproject{os.sep}{doxy_dir}{os.sep}docs{os.sep}xml'
        print(f'==> {cmd}')
        rc = subprocess.call(cmd, shell=True)
        if rc:
            sys.exit(rc)


# -- Project information -----------------------------------------------------

project = 'PJPROJECT'
copyright = '2020, Teluu'
author = 'Teluu Team'

# The full version, including alpha/beta/rc tags
release = '2.10'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'breathe',
    'sphinx_rtd_theme'
]

breathe_projects = { 
    "pjlib": "pjproject/pjlib/docs/xml", 
    "pilib_util": "pjproject/pjlib-util/docs/xml",
    "pjnath": "pjproject/pjnath/docs/xml",
    "pjmedia": "pjproject/pjmedia/docs/xml",
    "pjsip": "pjproject/pjsip/docs/xml",
}


# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['pjproject/*', '*_8c']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

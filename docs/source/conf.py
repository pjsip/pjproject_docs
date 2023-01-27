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
import re
import subprocess
import sys


# Which pjproject tag to checkout to create the documentation.
# Set to "master" to checkout the latest version
pjproject_tag = 'master'

# Doxygen XML files to be sanitized because it contains characters causing XML parsing to fail
sanitize_xml_files = [
    'pjproject/pjmedia/docs/xml/group__PJMED__G7221__CODEC.xml',
    'pjproject/pjnath/docs/xml/group__nat__intro.xml'
]


# Run doxygen if were in RTD
is_in_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if is_in_rtd:
    if os.path.exists('source/'):
        os.chdir('source')
    
    # Update pjproject git submodule to the specified version
    cmd = f"""cd pjproject && git checkout {pjproject_tag}"""
    print(f'==> {cmd}')
    rc = subprocess.call(cmd, shell=True)
    if rc:
        sys.exit(rc)

    # Run configure so that macros are declared more properly
    cmd = f"""cd pjproject && ./configure && make clean-doc"""
    print(f'==> {cmd}')
    rc = subprocess.call(cmd, shell=True)
    if rc:
        sys.exit(rc)

    pj_components = ['pjlib', 'pjlib-util', 'pjnath', 'pjmedia', 'pjsip']
    
    # doxygen
    for doxy_dir in pj_components:
        cmd = f'cd pjproject{os.sep}{doxy_dir} && doxygen docs/doxygen.cfg'
        print(f'==> {cmd}')
        rc = subprocess.call(cmd, shell=True)
        if rc:
            sys.exit(rc)
    
    # Sanitize XML files
    for fname in sanitize_xml_files:
        if not os.path.exists(fname):
            print(f'Warning: file {fname} does not exist')
            continue
        
        with open(fname, 'rb') as f:
            b = f.read()
    
        txt = b.decode('utf-8', errors='ignore')
        with open(fname, 'wt') as f:
            f.write(txt)

    # breathe
    for doxy_dir in pj_components:
        api_dir = 'pjlib_util' if doxy_dir=='pjlib-util' else doxy_dir
        cmd = f'breathe-apidoc -f -g group -m -p {api_dir} ' \
              f'-o api{os.sep}generated{os.sep}{api_dir} ' \
              f'pjproject{os.sep}{doxy_dir}{os.sep}docs{os.sep}xml'
        print(f'==> {cmd}')
        rc = subprocess.call(cmd, shell=True)
        if rc:
            sys.exit(rc)

        files = ['filelist.rst', 'grouplist', 'structlist.rst', 'unionlist.rst']
        for f in files:
            try:
                os.remove(f'api{os.sep}generated{os.sep}{api_dir}{os.sep}{f}')
            except:
                pass


# -- Project information -----------------------------------------------------

project = 'PJSIP Project'
copyright = '2022, Teluu'
author = 'Teluu Team'

# Find pjproject directory to open version.mak
pj_dirs = ['source/pjproject', 'pjproject']
pj_dir = None
for d in pj_dirs:
    if os.path.isdir(d):
        pj_dir = d
        break
if not pj_dir:
    raise RuntimeError(f'Unable to find pjproject directory')

# Parse pjproject version
with open(f'{pj_dir}/version.mak', 'rt') as f:
    doc = f.read()
lines = doc.splitlines()
vers = {}
for line in lines:
    m = re.search(r'(PJ_VERSION_[A-Z]+)\s*:=\s*(.*)', line)
    if m:
        vers[m.group(1)] = m.group(2)
#print(vers)
pj_version = f"{vers['PJ_VERSION_MAJOR']}.{vers['PJ_VERSION_MINOR']}"
if vers.get('PJ_VERSION_REV',''):
    pj_version += f".{vers['PJ_VERSION_REV']}"
if vers.get('PJ_VERSION_SUFFIX',''):
    pj_version += f"{vers['PJ_VERSION_SUFFIX']}"

print(f'Using pjproject version {pj_version}')

# The full version, including alpha/beta/rc tags
release = pj_version


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'breathe',
    'sphinx_rtd_theme',
    'recommonmark',
    'sphinx_copybutton',
    'sphinx.ext.extlinks',
]

source_parsers = {
   '.md': 'recommonmark.parser.CommonMarkParser',
}

source_suffix = ['.rst', '.md']

breathe_projects = { 
    "pjlib": "pjproject/pjlib/docs/xml", 
    "pjlib_util": "pjproject/pjlib-util/docs/xml",
    "pjnath": "pjproject/pjnath/docs/xml",
    "pjmedia": "pjproject/pjmedia/docs/xml",
    "pjsip": "pjproject/pjsip/docs/xml",
}

html_theme_options = {
    'navigation_depth': 3,
    'collapse_navigation': False,
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['pjproject/*', '*_8c']

extlinks = {
    'pr': ('https://github.com/pjsip/pjproject/pull/%s', '#%s'),
    'issue': ('https://github.com/pjsip/pjproject/issues/%s', '#%s'),
    'sourcedir' : ('https://github.com/pjsip/pjproject/tree/master/%s', '%s'),
    'source': ('https://github.com/pjsip/pjproject/blob/master/%s', '%s'),

    # already in Sphinx. Will emit annoying warning if redefined.
    #'rfc': ('https://datatracker.ietf.org/doc/html/rfc%s', 'RFC %s'),
}

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# These paths are either relative to html_static_path
# or fully qualified paths (eg. https://...)
html_css_files = [
    'css/custom.css',
]

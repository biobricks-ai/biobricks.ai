# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import subprocess, os

commit_id = os.environ.get('SELF_REV') or subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip().decode('ascii')
print(commit_id)
stable_version = os.environ.get('STABLE_VERSION')
versions = [
    ['latest', '/latest/'],
    ['stable', '/stable/'],
  ]
if stable_version:
  versions.append([stable_version, '/' + stable_version + '/'])
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'BioBricks'
copyright = '2023, Luechtefeld, Jaramillo'
author = 'Luechtefeld, Jaramillo'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []



# The root toctree document.
root_doc = "contents"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_favicon = 'favicon.ico'
html_show_copyright = False
html_show_sphinx = False
html_static_path = ['_static']
html_theme = 'sphinx_rtd_theme'
html_context = {
  # 'current_version': os.environ.get('CURRENT_VERSION', 'latest'),
  'display_github': True,
  'github_user': 'biobricks-ai',
  'github_repo': 'biobricks',
  'github_version': commit_id + '/docs/',
  'versions': versions,
}
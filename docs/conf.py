import os
import sys
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
# print(sys.executable)
#
# sys.path.insert(0, os.path.abspath(
#     '/Users/spod/Library/Caches/pypoetry/virtualenvs/homework-2-12-PxtXp1Z4-py3.10/bin/python')
#                 )
#
# # Добавляем путь к папке с модулями в переменную окружения PYTHONPATH
# os.environ['PYTHONPATH'] = os.path.abspath('path/to/your/module/folder')


sys.path.append(os.path.abspath('..'))
# sys.path.append(os.path.abspath('../..'))
# sys.path.insert(0, os.path.abspath('../'))
# sys.path.insert(0, os.path.abspath('..'))
# sys.path.insert(0, os.path.abspath('../..'))
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) #Olga
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'path', 'to', 'module', 'folder')))

project = 'Rest-API Homework 2.14'
copyright = '2023, SPod'
author = 'SPod'
release = '1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'nature'
html_static_path = ['_static']

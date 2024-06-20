#!/bin/bash

# Create a VEnv for Python 3.11.9
pyenv install 3.11.9
pyenv virtualenv 3.11.9 data-science-introduction
pyenv activate data-science-introduction

# Install General Dependencies
pip install --upgrade pip
pip install ipython
pip install poetry
poetry config virtualenvs.in-project true
poetry --version

# create poetry project and add dependencies
poetry new data-science-project
cd data-science-project
poetry add numpy pandas pandera pydantic tzdata openpyxl beautifulsoup4 matplotlib seaborn psycopg2-binary sqlalchemy scikit-learn xgboost uvicorn fastapi jupyterlab
poetry add -G dev black pylint pytest click pre-commit 
pip install ydata-profiling

# Restart shell
exec "$SHELL"
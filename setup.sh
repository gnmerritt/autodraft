#!/bin/bash -e

# Sets up venv & installs necessary stuff

virtualenv venv/

source venv/bin/activate

pip install sqlalchemy

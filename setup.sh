#!/bin/bash -e

# prereq: sudo easy_install virtualenv

# Sets up venv & installs necessary stuff
virtualenv --no-site-packages venv/

source venv/bin/activate

easy_install ipython django

echo "All set, now to get started do:"
echo "  source venv/bin/activate"

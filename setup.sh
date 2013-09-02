#!/bin/bash -e

# prereq: sudo easy_install virtualenv

# Sets up venv & installs necessary stuff
virtualenv --no-site-packages venv/

source venv/bin/activate

easy_install ipython django South simplejson readline
easy_install django-nose django-brake redis python-dateutil

echo "All set, now to get started do:"
echo "  source venv/bin/activate"
echo ""
echo "some commands to run:"
echo "./manage.py syncdb (builds your DB)"
echo "./manage.py import_teams (adds Nfl Teams to DB)"
echo "./manage.py import_positions (adds Nfl Positions to DB)"

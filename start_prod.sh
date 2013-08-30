#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR
source venv/bin/activate
python autodraft/manage.py runserver --settings autodraft.prod-settings 0.0.0.0:8000

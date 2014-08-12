#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR
source venv/bin/activate
python autodraft/manage.py run_gunicorn --settings autodraft.prod-settings -b 192.168.0.42:8000 -w 4

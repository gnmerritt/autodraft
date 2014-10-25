#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
HOST_IP=`ifconfig eth0 | awk '/t addr:/{gsub(/.*:/,"",$2);print$2}'`
CPUS=`grep -c ^processor /proc/cpuinfo`
JOBS=$(($CPUS + 1))
cd $DIR
source venv/bin/activate
python autodraft/manage.py run_gunicorn \
       --settings autodraft.prod-settings \
       -b ${HOST_IP}:8000 \
       -w $JOBS \
       --timeout 120

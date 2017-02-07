#!/bin/bash

source /home/galaxy/galaxy-maintenance/maintenance_local_env.sh
source /home/galaxy/galaxy/.venv/bin/activate
/home/galaxy/galaxy-maintenance/scripts/lifeportal_usage_report/lifeportal_usage_report.py

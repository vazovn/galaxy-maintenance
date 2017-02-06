#!/bin/bash

source /home/galaxy/galaxy_maintenance/maintenance_local_env.sh
source /home/galaxy/galaxy/.venv/bin/activate
/home/galaxy/galaxy_maintenance/scripts/mas_projects_maintenance/mas_projects_management.py

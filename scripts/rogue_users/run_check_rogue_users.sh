#!/bin/bash

source /home/galaxy/galaxy_maintenance/maintenance_local_env.sh
source /home/galaxy/galaxy/.venv/bin/activate
/home/galaxy/galaxy_maintenance/scripts/rogue_users/check_rogue_users.py


#!/bin/bash

source /home/galaxy/galaxy_mantenance_scripts_and_info/maintenance_local_env.sh
source /home/galaxy/galaxy/.venv/bin/activate
./check_rogue_users.py


#!/bin/bash

source GALAXYUSERHOMEPATH/galaxy-maintenance/maintenance_local_env.sh
${GALAXYUSERHOME}/galaxy-maintenance/scripts/rogue_users/check_rogue_users.py

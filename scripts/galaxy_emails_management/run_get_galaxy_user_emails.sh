#!/bin/bash

source /home/galaxy/galaxy-maintenance/maintenance_local_env.sh
source /home/galaxy/galaxy/.venv/bin/activate
/home/galaxy/galaxy-maintenance/scripts/galaxy_emails_management/get_galaxy_user_emails.py

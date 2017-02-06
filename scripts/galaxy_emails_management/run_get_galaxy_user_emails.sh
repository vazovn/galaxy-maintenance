#!/bin/bash

source /home/galaxy/galaxy_maintenance/maintenance_local_env.sh
source /home/galaxy/galaxy/.venv/bin/activate
sudo -E /home/galaxy/galaxy_maintenance/scripts/galaxy_emails_management/get_galaxy_user_emails.py

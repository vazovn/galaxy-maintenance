
# Galaxy maintenance scripts and info

## 1. The repo contains the following scripts:

    mas_projects_maintenance/run_mas_projects_management.sh
    
a script collecting the information about the MAS projects for every 
Galaxy user. This script is run as a cron job (owned by galaxy user). 

    galaxy_emails_management/run_get_galaxy_user_emails.sh

a script collecting the emails of all galaxy users. This script is 
run as a cron job (owned by root). 

    manipulate_project_allocations/run_manipulate_allocations_end_date.sh

a script allowing to modify the end date of every galaxy project. 
This script is run by root only.

    lifeportal_usage_report/run_lifeportal_usage_report.sh

a script displaying the usage for all galaxy projects (default project
included)

    rogue_users/run_check_rogue_users.sh

a script displaying the resources used by the users with access to AIR, BIR and CLOTU


## 2. The scripts can be installed either separately (after the Galaxy installation) or as a part of the entire Galaxy installation process

For a Galaxy-independent installation, set the following env variables in the file _deploy-galaxy-maintenance-self-standing.sh_ and run it: 

1. GALAXYTREE=/home/galaxy/galaxy
2. GALAXYUSERHOME=/home/galaxy/

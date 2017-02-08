#!/bin/bash

# This script must be run _ONLY_ to install galaxy-maintenance-kit to a server with 
# already installed galaxy. 

#For a Galaxy-independent installation, set the following env variables:
GALAXYTREE=/home/galaxy/galaxy
GALAXYUSERHOME=/home/galaxy/

if [ -f ${GALAXYTREE}/config/local_env.sh ]; then
        echo "local_env.sh found, OK ..."
else
        echo "local_env.sh not found, please check before deploying maintenance scripts!!"
        exit 1
fi

cp deploy-galaxy-maintenance-self-standing.sh ..
cd ..
chmod u+x deploy-galaxy-maintenance-self-standing.sh

if [ -e "galaxy-maintenance" ]; then
    # clean the repo and clone again
    rm -rf galaxy-maintenance
    git clone https://${USER}@bitbucket.usit.uio.no/scm/ft/galaxy-maintenance.git
else
    git clone https://${USER}@bitbucket.usit.uio.no/scm/ft/galaxy-maintenance.git
fi

sudo chown -R galaxy:galaxy galaxy-maintenance
sudo chmod go-x galaxy-maintenance/scripts/galaxy_emails_management/*
sudo chmod go-x galaxy-maintenance/scripts/manipulate_project_allocations/*
    
sudo mv galaxy-maintenance ${GALAXYUSERHOME}/

echo "Galaxy maintenance kit installed in galaxy-maintenance! Do not forget to set the cron jobs for :\ngalaxy email management (root) and mas_projects_maintenance (galaxy)!"

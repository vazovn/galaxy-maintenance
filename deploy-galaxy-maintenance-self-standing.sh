#!/bin/bash

#For a Galaxy-independent installation, set the following env variables:

GALAXYTREE=/home/galaxy/galaxy
GALAXYUSERHOME=/home/galaxy/

if [ -f ${GALAXYTREE}/config/local_env.sh ]; then
        echo "local_env.sh found, OK ..."
else
        echo "local_env.sh not found, please check before deploying maintenance scripts!!"
        exit 1
fi

git clone https://${USER}@bitbucket.usit.uio.no/scm/ft/galaxy-maintenance.git 

sudo chown -R galaxy:galaxy galaxy-maintenance
sudo chown -R root:root galaxy-maintenance/scripts/galaxy_emails_management/
sudo chmod go-x galaxy-maintenance/scripts/galaxy_emails_management/*
sudo chown -R root:root galaxy-maintenance/scripts/manipulate_project_allocations/
sudo chmod go-x galaxy-maintenance/scripts/manipulate_project_allocations/*
    
sudo mv galaxy-maintenance ${GALAXYUSERHOME}/

echo "Galaxy maintenance kit installed in galaxy-maintenance! Do not forget to set the cron jobs for :\ngalaxy email management (root) and mas_projects_maintenance (galaxy)!"

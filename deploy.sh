#!/bin/bash

# Activate one of the

# galaxy-integrated install : built into galaxy installation
# source settings
#. settings.sh

## galaxy independent install : can be run after galaxy installation
#GALAXYTREE=/home/galaxy/galaxy
#GALAXYUSERHOME=/home/galaxy/
#GALAXY_ABEL_MOUNT=1


git clone https://${USER}@bitbucket.usit.uio.no/scm/ft/galaxy-maintenance.git 

if [ -f ${GALAXYTREE}/config/local_env.sh ]; then
        echo "local_env.sh found, OK ..."
else
        echo "local_env.sh not found, please check before deploying maintenance scripts!!"
        exit 1
fi

## Customize Galaxy platform with Cluster and Project Management issues
if [ "${GALAXY_ABEL_MOUNT}" == "1" ]; then
    
    sudo chown -R galaxy:galaxy galaxy-maintenance
    sudo chown -R root:root galaxy-maintenance/scripts/galaxy_emails_management/
    sudo chmod go-x galaxy-maintenance/scripts/galaxy_emails_management/*
    sudo chown -R root:root galaxy-maintenance/scripts/manipulate_project_allocations/
    sudo chmod go-x galaxy-maintenance/scripts/manipulate_project_allocations/*
    
    sudo mv galaxy-maintenance ${GALAXYUSERHOME}/
fi



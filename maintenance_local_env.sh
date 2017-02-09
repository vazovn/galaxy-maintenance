
# used in this script
GALAXYTREE=
# used in the run-* script of the maintenance kit
GALAXYUSERHOME=

source ${GALAXYTREE}/config/local_env.sh
source ${GALAXYTREE}/.venv/bin/activate

## used in ./additional_python_galaxy_packs/get_galaxy_user_emails.py
export GALAXY_USER_EMAIL_LIST="/work/var/emaillist.lifeportal-users"

## DB config
GALAXYDB_STRING=$(cat /home/galaxy/galaxy/config/galaxy.ini | grep postgresq | awk '{print $3}')

if [ -n "$GALAXYDB_STRING"} ]; then
    export GALAXYDB_STRING
    #echo "GALAXYDB_STRING" $GALAXYDB_STRING
else
    echo "Galaxy Database not accessible"
fi

## EXTERNAL DBs
EXTERNAL_DBS_LINK_NAME="/home/galaxy/galaxy/lib/usit/external_dbs"

if [ -d "${EXTERNAL_DBS_LINK_NAME}" ]; then
    export EXTERNAL_DBS_LINK_NAME
    echo "EXTERNAL_DBS_LINK_NAME" $EXTERNAL_DBS_LINK_NAME
else
    echo "External DB directory not found"
fi

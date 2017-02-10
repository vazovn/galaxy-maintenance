#!/bin/env python

import os, sys
import ConfigParser
from sqlalchemy import *
import shutil

if os.environ['GALAXYDB_STRING'] :
    GALAXYDB_STRING = os.environ['GALAXYDB_STRING']
else:
    print "GALAXYDB not accessible!"
    sys.exit()
    
if os.environ['EXTERNAL_DBS_LINK_NAME'] :
    EXTERNAL_DBS = os.environ['EXTERNAL_DBS_LINK_NAME']
else:
    print "EXTERNAL_DBS not found!"
    sys.exit()

if os.environ['GALAXY_USER_EMAIL_LIST'] :
    GALAXY_USER_EMAIL_LIST = os.environ['GALAXY_USER_EMAIL_LIST']
else:
    print "GALAXY_USER_EMAIL_LIST not found"
    sys.exit()

dir_path = os.path.dirname(os.path.realpath(__file__))

# Read (or create) config file
config = ConfigParser.ConfigParser()
if os.path.isfile(dir_path+'/collect_galaxy_emails.cfg'):
    config.read(dir_path+'/collect_galaxy_emails.cfg')
else:
    print "No config file found. Creating new"
    config.add_section('db')
    config.set('db', 'uri', GALAXYDB_STRING)
    config.set('db', 'table_name', 'galaxy_user')  

    with open(dir_path+'/collect_galaxy_emails.cfg', 'wb') as configfile:
        config.write(configfile)

# If run with any argument, exit after creating config
if len(sys.argv) > 1:
    print "Please fill out {}".format('collect_galaxy_emails')
    exit(0)

# Database connection
engine = create_engine(config.get('db', 'uri'), encoding='utf-8')
metadata = MetaData(engine)
connection = engine.connect()


emails = []
result = connection.execute("select email from galaxy_user where deleted = 'f' and purged = 'f'")
for row in result:
    emails.append(row['email'])
    
connection.close()

#print emails

emails_file_local = EXTERNAL_DBS+'/galaxy_user_emails.txt'
    
f=open(emails_file_local, 'w')
for email in emails :
    f.write(email+'\n')
f.close()

shutil.move(emails_file_local, GALAXY_USER_EMAIL_LIST)




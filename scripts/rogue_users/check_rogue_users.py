#!/bin/env python

## This script show all the tools used by the users registered for CLOTU (lp39) and BIR (lp40). They are supposed to use exclusively CLOTU and BIR!!
## The results are ordered in desc date order

import os, sys, logging, threading, time, string
from sqlalchemy import *
import subprocess
import re
from pprint import pprint

if os.environ['GALAXYDB_STRING'] :
    GALAXYDB_STRING = os.environ['GALAXYDB_STRING']
else:
    print "GALAXYDB not accessible!"
    sys.exit()

application_db_engine = create_engine(GALAXYDB_STRING, encoding='utf-8')
connection = application_db_engine.connect()


tmp_members = []
bir_members = []
clotu_members = []

get_all_bir_users_command = "sudo -u gold /opt/gold/bin/glsproject -p lp40 --show Users"
p = subprocess.Popen(get_all_bir_users_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
p.wait()

for line in p.stdout.readlines():
    tmp_members = line.strip()
bir_members = tmp_members.split(",")
del bir_members[0]


get_all_clotu_users_command = "sudo -u gold /opt/gold/bin/glsproject -p lp39 --show Users"
p = subprocess.Popen(get_all_clotu_users_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
p.wait()

for line in p.stdout.readlines():
    tmp_members = line.strip()
clotu_members = tmp_members.split(",")
del clotu_members[0]

all_bir_and_clotu = list(set(bir_members) | set(clotu_members))
quoted_all_bir_and_clotu = []

for i in all_bir_and_clotu : 
    if i == 'n.a.vazov@usit.uio.no' :
      continue
    i = "'"+i+"'"
    quoted_all_bir_and_clotu.append(i)

users = ', '.join(quoted_all_bir_and_clotu)

# print "ALL BIR AND CLOTU USERS : ", users

result = connection.execute("select\
                                    date_trunc('minutes', job.create_time::timestamp) as create_time,\
                                    date_trunc('minutes', job.update_time::timestamp) as update_time, \
                                    job.id, \
                                    job.tool_id,\
                                    galaxy_user.email \
                                from \
                                    job,\
                                    galaxy_user \
                                where \
                                    galaxy_user.id = job.user_id \
                                        and \
                                    galaxy_user.email in ({}) \
                                order by \
                                    job.create_time \
                                desc".format(users))

all_jobs = []

for row in result:
    all_jobs.append(row)

column_titles = ["START_TIME", "END_TIME", "GALAXY_JOB_ID", "USED_TOOL", "USER_EMAIL"]
title_format = ''
for title in column_titles :
    title_format = title_format + title + " "*(25-len(title))
print title_format


for job in all_jobs :
    display_format = ''
    for el in job :
        display_format = display_format + str(el) + " "*(25-len(str(el)))
    print display_format


#!/bin/env python
"""
    Lists all GOLD projects, needs sqlalchemy and psycopg2 from yum :
    sudo yum install python27-python-sqlalchemy.x86_64 python-sqlalchemy.x86_64
    sudo yum install python27-python-psycopg2.x86_64 python-psycopg2.x86_64
"""
 
import os, sys, logging, threading, time, string, datetime
from sqlalchemy import *
import re


DBvalue = None
report_file = None

filehandler=open('/home/galaxy/galaxy/config/local_env.sh', 'r')
for line in filehandler :
    if re.search('export GOLDDB', line) :
          DBvalue = line.split('"')[1]


if DBvalue is not None:

    application_db_engine = create_engine(DBvalue, encoding='utf-8')

    metadata = MetaData(application_db_engine)
    connection = application_db_engine.connect()

    result = connection.execute("select\
                                                                   g_organization,\
                                                                   g_name,\
                                                                   g_active,\
                                                                   g_description\
                                                           from\
                                                                   g_project\
                                                           where\
                                                                   g_active = 'True' ")

    project_data = []
    project_data_users = []
    project_list = []
    users_list = {}
    projects_amount_start_end = {}
    final_list = []
    gx_default_usage = {}
    
    if not result :
       print "No projects available!"
              
    for row in result:
       if not re.search("@",str(row[0])) :
             pass
       elif re.search("root@",str(row[0])) :
             pass
       else :
             project_data.append(row)
             project_id = "'"+row[1]+"'"
             project_list.append(project_id)
    
    string_project_list = ','.join(project_list)
    
    users = connection.execute("select\
                                                                  g_project,\
                                                                  array_to_string(array_agg(g_name),',')\
                                                          from\
                                                                  g_project_user\
                                                         where\
                                                                  g_project in ( %s ) \
                                                         group by 1" % string_project_list)
    
    #store users in a hash : key - project_name (lpXX), value - user list
    for row in users:
       users = row[1].replace(",",":")
       users_list[row[0]] = users

    #append user list to project data array
    for k in users_list :
       for p in project_data :
            if k == p[1] :
               p_list = list(p)
               p_list.insert(2,users_list[k])
               project_data_users.append(p_list)
               continue
             
    #print "Admin is True : Accounting : All GOLD projects WITH USERS ", project_data_users
    
    
    amounts_and_time  = connection.execute("select\
                                                                                           g_account_project.g_name,\
                                                                                           g_allocation.g_id,\
                                                                                           g_allocation.g_amount,\
                                                                                           g_allocation.g_start_time,\
                                                                                           g_allocation.g_end_time\
                                                                                    from\
                                                                                           g_account_project,\
                                                                                           g_allocation\
                                                                                   where\
                                                                                           g_account_project.g_name in ( %s ) \
                                                                                           and\
                                                                                           g_account_project.g_account = g_allocation.g_account\
                                                                                   order by\
                                                                                           g_allocation.g_id " % string_project_list )
    
    
    for row in amounts_and_time :
         amount = "{0:.2f}".format(row[2]/3600)
         start = datetime.datetime.fromtimestamp(row[3]).strftime('%Y-%m-%d')
         stop = datetime.datetime.fromtimestamp(row[4]).strftime('%Y-%m-%d')
         projects_amount_start_end[row[0]] = [amount, start, stop]
         
     
    for p in projects_amount_start_end :
         for r in project_data_users :
                if p == r[1] :
                     r.insert(4,projects_amount_start_end[p][0])
                     r = r + projects_amount_start_end[p][1:]
                     final_list.append(r)
                     continue
    
  
    ## GX_DEFAULT project
    gx_default = connection.execute("select\
                                                                     g_allocation.g_id,\
                                                                     g_allocation.g_amount,\
                                                                     g_account.g_name\
                                                         from\
                                                                     g_allocation,\
                                                                     g_account\
                                                         where\
                                                                     g_account.g_name  in (select g_name from g_account where g_name like '%%_gx_default' )\
                                                                     and\
                                                                     g_account.g_id = g_allocation.g_account\
                                                         order by\
                                                                     g_allocation.g_id " )
                              
                              
    connection.close()
    
    for row in gx_default:
         gx_default_usage[row[2]] = "{0:.2f}".format(row[1]/3600)
    
    #print "Admin is True : Accounting : All GOLD projects FINAL LIST ",  final_list
    #print "Admin is True : Accounting : All GOLD projects GX DEFAULT LIST ", gx_default_usage
    

    ## Write to file if needed for report
    column_titles = ["OWNER", "PROJECT ID", "REMAINING AMOUNT", "START", "END"]
    title_format = ''
    
    print "\n=== LP USAGE ===\n"
    
    for title in column_titles :
              title_format = title_format + title + " "*(35-len(title))
    print title_format

    for elements in final_list:
         display_format = ''
         loop_array = elements[0:2]+elements[4:5]+elements[6:]
         for el in loop_array:
             display_format = display_format + str(el) + " "*(35-len(str(el)))
         print display_format

    print "\n=== GX_DEFAULT USAGE ===\n"

    for key, value in gx_default_usage.iteritems() :
         gx_display_format = str(key) + " "*(100-len(str(key)))+ value
         print gx_display_format
         
else :
    print "Missing  GOLDDB"



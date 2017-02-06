#!/bin/env python

"""
This script must be run as a cron job (owner : galaxy). It parses the MAS project file, creates and populates the gold db table 'g_mas_projects':

uname
status
projects
mas_email
uio_email

How it works:

NEW TABLE (INSERT)
If the table g_mas_projects is not found, it will be created and the first 4 fields will be populated.

EXISTING TABLE (UPDATE)
If the table g_mas_projects exists, it will ONLY be updated for 'status', 'projects' and 'mas_email' columns!

NEW USER IN EXISTING TABLE (INSERT)
If, during the update, a new user is detected in the MAS project file, the first 4 fields will be populated for this user.
"""


import os, sys, logging, threading, time, string, datetime
import re
import subprocess
from sqlalchemy import *


# If run with any argument, exit after creating config
if len(sys.argv) > 1:
    print "This script does not take any arguments!"
    sys.exit()

if os.environ['GOLDDB'] :
    GOLDDB = os.environ['GOLDDB']
else:
    print "GOLDDB not accessible for MAS projects update!"
    sys.exit()


## DB table creation and population
application_db_engine = create_engine(GOLDDB, encoding='utf-8')
metadata = MetaData(application_db_engine)
connection = application_db_engine.connect()

def parse_mas_file() :
		
		all_per_user_data = []
		all_users_data = []
		
		## Read file from MAS
		f=open('/work/var/user-info', 'r')
		
		take_lines = False
		
		uname_flag = 0
		status_flag = 0
		projects_flag = 0
		email_flag = 0
		
		for line in f :
			
			take_lines = take_lines
			all_per_user_data = all_per_user_data
			
			# flags
			uname_flag = uname_flag
			status_flag = status_flag
			projects_flag = projects_flag
			email_flag = email_flag
			
			if re.search( "<.*>", line) :
				take_lines = True
			
			if take_lines == True:
				if re.search( "uname", line) :
					uname = line.split()[1]
					uname_flag = 1
					all_per_user_data.append(uname)
				if re.search( "status", line) :
					status = line.split()[1]
					status_flag = 1
					all_per_user_data.append(status)
				if re.search( "projects", line) :
					project_line = line.split()
					if len(project_line) == 2:
						projects = project_line[1]
						projects_flag = 1
						all_per_user_data.append(projects)
					else :
						projects = "None"
						projects_flag = 1
						all_per_user_data.append(projects)
				if re.search( "email", line) and not re.search( "email address", line)  :
						email = line.split()[1]
						email_flag = 1
						all_per_user_data.append(email.lower())
				
				if re.search( "</.*>", line) :
					
					## Take user_data
					if uname_flag == 1 and status_flag == 1 and projects_flag == 1 and email_flag == 1 :
						#print "TAKE IN USER DATA :", all_per_user_data
						all_users_data.append(all_per_user_data)
						all_per_user_data = []
						uname_flag = 0
						status_flag = 0
						projects_flag = 0
						email_flag = 0
					## Skip this block data
					else :
						print "Skipping MAS system user :", all_per_user_data
						all_per_user_data = []
						uname_flag = 0
						status_flag = 0
						projects_flag = 0
						email_flag = 0
					
					take_lines = False
                    
		return all_users_data


def create_db() :
		
		## Check if the table g_mas_projects exists
		
		brand_new_table = False
		
		result  = connection.execute("select table_name from information_schema.tables where table_name = 'g_mas_projects'")
		if result.rowcount > 0 :
			print "Table g_mas_projects exists"
			
		else :
			connection.execute("create sequence g_mas_projects_seq")
			connection.execute("create table g_mas_projects  ( \
									id int NOT NULL DEFAULT nextval('g_mas_projects_seq'),\
									uname varchar(20) NOT NULL,\
									status varchar(20),\
									projects varchar(200), \
									mas_email varchar(200) NOT NULL, \
									uio_email varchar (200) ) " )
			brand_new_table = True
  			print "Table g_mas_projects created"

		return brand_new_table

def populate_db (all_users_data, brand_new_table = False ) :
		
        # update if table is already populated
		if brand_new_table == False:
			print "Updating the g_mas_projects ... "
			for userinfo in all_users_data:
				## check consistency of every item before populating to database
				if userinfo[0] != '' and userinfo[1] != '' and  userinfo[2] != ''  and userinfo[3] != '' and re.search("@",userinfo[3]):  
					update_result = connection.execute("update g_mas_projects\
		                                                        set \
		                                                            status='%s',\
		                                                            projects='%s',\
                                                                    mas_email='%s'\
		                                                        where\
		                                                            uname = '%s'" % (userinfo[1], userinfo[2], userinfo[3], userinfo[0] ) ) 
					if update_result.rowcount > 0 :
						next
					else :
						connection.execute("insert into g_mas_projects (\
		                                                uname, status, projects, mas_email )\
                                                    values ('%s','%s','%s','%s') " %  ( userinfo[0], userinfo[1], userinfo[2], userinfo[3] ) )
				else:
					print "Error while updating MAS_project table \
                                                        uname: %s, \
                                                        status : %s, \
                                                        projects : %s, \
                                                        mas_email : %s " % (userinfo[0], userinfo[1],userinfo[2],userinfo[3])
			
			print "GOLD table updated with mas project info!"
		
		# populate with data (insert) if brand_new_table
		else :
			print "Bootstraping the g_mas_projects table... "
			for userinfo in all_users_data:
				## check consistency of every item before populating to database
				if userinfo[0] != '' and userinfo[1] != '' and  userinfo[2] != ''  and userinfo[3] != '' and re.search("@",userinfo[3]): 
					connection.execute("insert into g_mas_projects\
		                                            (uname, status, projects, mas_email )\
                                                values (\
                                                    '%s','%s','%s','%s') " % (userinfo[0], userinfo[1], userinfo[2], userinfo[3]) )
				else:
					print "Error while populating MAS_project table \
                                                            uname: %s,\
                                                            status : %s,\
                                                            projects : %s,\
                                                            mas_email : %s " % (userinfo[0], userinfo[1],userinfo[2],userinfo[3])
			
			print "GOLD table populated with mas project info!"
		
		connection.close()


if __name__ == '__main__':
    brand_new_table = create_db()
    all_users_data = parse_mas_file()
    populate_db (all_users_data, brand_new_table )

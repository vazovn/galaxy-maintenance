#!/bin/env python

'''
Script which configures the upload of abel (cluster) files from the cluster home directory to Galaxy.
'''

import os, sys, logging, stat
import pwd
import grp
import re

try:
    email = sys.argv[1]
except:
    print "Usage ./add_upload_directory.py <galaxy_username (email)> <cluster_username>"
    exit(0)
    
try:
    username = sys.argv[2]
except :
    print "Usage ./add_upload_directory.py <galaxy_username (email)> <cluster_username>"
    exit(0)

abel_upload_dir = None
galaxy_upload_dir = None

## Necessary checks

if os.path.isdir("/cluster/home/"+username):
   #### home_dir = "/cluster/home/"+username
   print "\n-------\nHome directory of user "+username+" : OK"
else:
   print "\nUser "+username+" does not have a homedir!\n"
   sys.exit('ERROR : The user does not have an Abel home directory')

if os.path.isdir("/cluster/home/"+username+"/"+email):
   abel_upload_dir = "/cluster/home/"+username+"/"+email
   print "-------\nThe abel upload directory is /cluster/home/"+username+"/"+email
else:
   sys.exit('ERROR : Upload directory /cluster/home/'+ username + '/' + email +' not defined in the user home directory!')
   

filehandler=open('/home/galaxy/galaxy-dist/startup_settings.sh', 'r')

for line in filehandler :
    if re.search('export ABEL_UPLOAD_DIRECTORY', line) :
          galaxy_upload_dir = line.split('"')[1]
          print "-------\nThis galaxy instance upload directory is : ", galaxy_upload_dir

if not galaxy_upload_dir:
    print "GALAXY UPLOAD DIRECTORY is missing"
    sys.exit('Define the upload directory for this galaxy instance in galaxy.ini (ftp)')

## Enable the upload

os.chdir(galaxy_upload_dir)

## if enabling upload for the first time : create the symlink in 
## galaxy_upload_dir (galaxy) -->> abel_upload_dir (cluster)
if not os.path.isdir(galaxy_upload_dir+email) :
    os.symlink(abel_upload_dir, email)
    print "Created symlink to the abel_upload_dir"

uid = pwd.getpwnam(username).pw_uid
gid = grp.getgrnam("galaxy").gr_gid
mode = 0o770

os.chown(abel_upload_dir, uid, gid)
os.chmod(abel_upload_dir, mode)

def change_ownership_and_permissions_recursive(path, uid, gid, mode):
    for root, dirs, files in os.walk(path, topdown=False):
        for dir in [os.path.join(root,d) for d in dirs]:
            os.chown(dir,uid, gid)
            os.chmod(dir, mode)
        for file in [os.path.join(root, f) for f in files]:
            os.chown(file,uid, gid)
            os.chmod(file, mode)
            
change_ownership_and_permissions_recursive(abel_upload_dir, uid, gid, mode)




print "=== Upload to Abel enabled for the user ==="+username

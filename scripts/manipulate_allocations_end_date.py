#!/bin/env python

'''
Script to modify end dates of the projects. The script actually modifies the end date of 
the allocations in GOLD.
'''


import os, sys, logging, threading, time, string
import subprocess
import re
from pprint import *


old_end_date = raw_input('Old end date to be replaced (YYYY-MM-DD): ')
new_end_date = raw_input('New end date to be inserted (YYYY-MM-DD) : ')
dry_run = raw_input('Is this a dry run (yes/no) : ')

if dry_run != 'yes' and dry_run != 'no' :
    print "Please precise if this is a dry run or not!"
    exit()


## Get the account id
command = "sudo /opt/gold/bin/glsalloc --show Id,EndTime | grep %s" % old_end_date
p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
p.wait()

#Contains the Ids of the allocations with the endtime to be modified
endDateList = []

for line in p.stdout.readlines():
         print line
         info = line.split()
         endDateList.append(info[0])
         
print "Allocation IDs whose EndTime will change ", endDateList

if dry_run == 'yes' :
    print "This was a dry run, for a real change answer 'no' when prompted!"
    exit()
            
            
for allocId in endDateList :
         command1 = "sudo /opt/gold/bin/gchalloc -e %s -i %s" % (new_end_date, allocId)
         p = subprocess.Popen(command1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
         p.wait()
        

## Final check of changes 
for allocId in endDateList :
        command2 = "sudo /opt/gold/bin/glsalloc --show Id,EndTime -i %s | grep %s" % (allocId,new_end_date)
        p = subprocess.Popen(command2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()
        
        for line in p.stdout.readlines():
             print line

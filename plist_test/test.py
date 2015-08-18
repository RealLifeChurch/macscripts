from FoundationPlist import *
import os
count = 0
plist = "/private/var/tmp/com.onset.plist"
if os.path.isfile(plist):
    plistDict = readPlist(plist)
    nothingToDo = False
else:
    nothingToDo = True

if count == 0:
    if plistDict['NameIsDone'] == "True":
        print "NameIsDone"
        count += 1

print count
print plistDict['NameIsDone']

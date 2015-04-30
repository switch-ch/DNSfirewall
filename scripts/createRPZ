#!/usr/bin/python
# This script expect a list of line-separated domains.
# From this list of domains, a RPZ will be created.
# The RPZ can then be used on a recurisve DNS server
# as a white- or blacklist, depending on the position
# of the RPZ and the rule.
# Author: Matthias Seitz <matthias.seitz@switch.ch>
 
import calendar
import time
import sys
 
SCRIPTUSAGE = "Usage: createRPZ.py [-v]\n"
SCRIPTUSAGE += "-v      verbose mode. Show debug infos"
 
RPZ_NAME = "whitelist.rpz."
DOMAINS_FILE_NAME = "domains.txt"
ZONE_FILE_NAME = "rpz_whitelist.zone"
 
# Timing values for the zone
ZONE_SERIAL = calendar.timegm(time.gmtime())
SLAVE_REFRESH_INTERVAL = 180    # 3min
SLAVE_RETRY_INTERVAL = 60       # 1min
SLAVE_EXPERIATION_TIME = 259200 # 3days
NXDOMAIN_CACHE_TIME = 180       # 3min
RECORD_TTL = 300                # 5min
 
def isVerboseMode():
        if len(sys.argv) > 1:
                if sys.argv[1] == "-v":
                        return True
                else:
                        return False
        else:
                return False
 
def printVerboseInfos(infos):
        print  "============================================================"
        print infos
        print
 
def collectAndPrintVerboseInfos():
        if isVerboseMode():
                verboseInfos = "Some verbose Text"
                printVerboseInfos(verboseInfos)
 
 
def getNumberOfLines(fileName):
        with open(fileName) as f:
                return sum(1 for _ in f)
 
def createZoneHeader():
        header = RPZ_NAME + "   " + str(RECORD_TTL) + " IN SOA  none. cert.switch.ch. " + str(ZONE_SERIAL) + " " + \
        str(SLAVE_REFRESH_INTERVAL) + " " + str(SLAVE_RETRY_INTERVAL) + " " + str(SLAVE_EXPERIATION_TIME) + " " + \
        str(NXDOMAIN_CACHE_TIME) + "\n"
        header += RPZ_NAME + "  " + str(RECORD_TTL) + " IN NS   LOCALHOST." + "\n"
 
        return header
 
def createZoneBody():
        body = ""
        try:
                with open(DOMAINS_FILE_NAME) as f:
                        domains = f.readlines()
                        for d in domains:
                                d = d.replace('\n','')
                                body += d + "." + RPZ_NAME + "          300 IN CNAME    .\n"
        except EnvironmentError:
                raise Exception("Error with handling the file: " + DOMAINS_FILE_NAME + \
                                "\nPossibly there is no such file.")
        return body
 
def writeZoneFile(header, body):
        try:
                f = open(ZONE_FILE_NAME, 'w')
                f.write(header)
                f.write(body)
                f.close()
 
                if isVerboseMode():
                        verboseInfos = "=== Zone content:\n\n"
                        verboseInfos += header
                        verboseInfos += body
                        printVerboseInfos(verboseInfos)
 
                print "zone " + RPZ_NAME + " created\n"
                print "number of lines: " + str(getNumberOfLines(ZONE_FILE_NAME))
        except EnvironmentError:
                raise Exception("Error with handling the file: " + ZONE_FILE_NAME + \
                                "\nPossibly no write permission for the directory.")
 
def createZone():
        try:
                header = createZoneHeader()
                body = createZoneBody()
                writeZoneFile(header, body)
 
        except Exception as e:
                print "Exception: " + str(e)
 
# handle parameters
if len(sys.argv) == 1:
        createZone()
 
elif len(sys.argv) == 2:
        if sys.argv[1] == "-v":
                createZone()
        else:
                print SCRIPTUSAGE
else:
        print SCRIPTUSAGE

#!/usr/bin/python
# This script expect a list of line separated domains.
# From this list of domains, a RPZ will be then created.
#
# The created RPZ can be used on a recursive DNS server
# as a white- or blacklist, depending on the position
# of the RPZ and the rule.
#
# Author: Matthias Seitz <matthias.seitz@switch.ch>

import calendar, re, time, sys

rpz_name = 'whitelist.rpz.'
domains_file_name = 'domains.txt'
zone_file_name = 'rpz_whitelist.zone'

# Timing values for the zone
zone_serial = calendar.timegm(time.gmtime())
slave_refresh_interval = 180    # 3min
slave_retry_interval = 60       # 1min
slave_experiation_time = 259200 # 3days
nxdomain_cache_time = 180       # 3min
record_ttl = 300                # 5min

def create_zone_header():
        header = rpz_name + '   ' + str(record_ttl) + ' IN SOA  none. cert.switch.ch. ' + str(zone_serial) + ' ' + \
        str(slave_refresh_interval) + ' ' + str(slave_retry_interval) + ' ' + str(slave_experiation_time) + ' ' + \
        str(nxdomain_cache_time) + '\n'
        header += rpz_name + '  ' + str(record_ttl) + ' IN NS   LOCALHOST.' + '\n'

        return header

def create_zone_body():
        body = ''
        try:
                with open(domains_file_name) as f:
                        domains = f.readlines()
                        # Remove empty elements
                        domains = filter(lambda x: not re.match(r'^\s*$', x), domains)
                        print 'Number of entries: ' + str(len(domains))
                        for d in domains:
                                d = d.replace('\n','')
                                body += d + '.' + rpz_name + '          300 IN CNAME    rpz-passthru.\n'
                                body += '*.' + d + '.' + rpz_name + '          300 IN CNAME    rpz-passthru.\n'
        except EnvironmentError:
                raise Exception('Error with handling the file: ' + domains_file_name + \
                                '\nPlease check if file exists.')
        return body

def write_zone_file(header, body):
        try:
                f = open(zone_file_name, 'w')
                f.write(header)
                f.write(body)
                f.close()
                print 'RPZ ' + rpz_name + ' created'
        except EnvironmentError:
                raise Exception('Error with handling the file: ' + zone_file_name + \
                                '\nPlease check if you have write permissions for the directory.')

def create_zone():
        try:
                header = create_zone_header()
                body = create_zone_body()
                write_zone_file(header, body)

        except Exception as e:
                print 'Exception: ' + str(e)

# === MAIN
if __name__ == '__main__':
    create_zone()

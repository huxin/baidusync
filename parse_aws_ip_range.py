import os
import json
import ipaddress
from collections import defaultdict


d = json.loads(open('ip-ranges.json', 'r').read())

service2ips = defaultdict(set)
regions = set()
for prefix in d['prefixes']:
    service = prefix['service']
    ip_prefix = prefix['ip_prefix']
    region = prefix['region']

    if region.startswith('us') and service == 'AMAZON':
        service = 'AMAZON-US'
    # expand ip prefix to ip address
    # for ip in ipaddress.ip_network(ip_prefix):
    #     service2ips[service].add(ip)
    service2ips[service].add(ip_prefix)


for service, prefixes in service2ips.iteritems():
    cnt = 0
    for p in prefixes:
        cnt += 2**(32-ipaddress.ip_network(p).prefixlen)
    print service, cnt

    with open("{}-{}.ip".format(service, cnt), 'w') as outf:
        for p in prefixes:
            print >>outf, p
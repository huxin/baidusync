#!/usr/bin/env python

import os
import sys
import subprocess32
import json
from multiprocessing import Pool, TimeoutError
import time
import ipaddress

# donwload ip range
# https://ip-ranges.amazonaws.com/ip-ranges.json

port_open_timeout = 0.2
curl_cmd_timeout = 4
max_proc = 20

def port_open(ip, port):
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(port_open_timeout)
    result = sock.connect_ex((ip, port))
    return result==0


def santize(s):
    n = ''
    for c in s:
        if ord(c) < 128:
            n += c
    return n

def curl_ip(ip):
    try:
        if not port_open(ip, 80):
            return [ip, 'port 80 not open']
        output = subprocess32.check_output(['curl', '-s', 'http://'+ip], timeout=curl_cmd_timeout)
        output = santize(output)
    except Exception as e:
        return json.dumps([ip, e.message])

    return json.dumps( [ip, output.replace("\n", " ").replace("/r", '')])




def scan_ips(ip_set, outfname):
    start_t = time.time()
    pool = Pool(processes=max_proc)
    with open(outfname, 'a') as outf:
        for i in pool.imap_unordered(curl_ip, list(ip_set)):
            print int(time.time()-start_t), i
            print >>outf, int(time.time()-start_t), i


if len(sys.argv) != 2:
    print sys.argv[0], "ip_list_file"
    exit(1)


ip_list = []
for p in open(sys.argv[1]):
    p = p.strip()
    if p.find('.') == -1:
        continue
    ip_list.append(p)

print "Found total:", len(ip_list), "IPs, start scanning:"
import random

res_file = sys.argv[1]+'.scan.res'

scanned_ip_set = set()
for l in open(res_file, 'r'):
    p = l.split("'")
    if len(p) < 2:
        continue
    ip =p[1]
    scanned_ip_set.add(ip)

print "Total IP #:", len(ip_list)
print "scanned ip #:", len(scanned_ip_set)
print "remaining: #", len(set(ip_list) - scanned_ip_set)
remain = list(set(ip_list) - scanned_ip_set)



random.shuffle(remain)
scan_ips(remain, res_file)


#scan_ips(set(['52.200.189.78', '52.200.189.77', '34.225.47.67', '34.203.109.236', '52.54.211.81']))
# ip = '52.200.189.78'
# port = 80
# print port_open(ip, port )

# print curl_ip('52.200.189.77')
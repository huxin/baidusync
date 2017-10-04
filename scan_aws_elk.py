#!/usr/bin/env python

import os
import sys
import subprocess
import json
from multiprocessing import Pool, TimeoutError
import time
import ipaddress

# donwload ip range
# https://ip-ranges.amazonaws.com/ip-ranges.json

port_open_timeout = 0.2
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
        output = subprocess.check_output(['curl', '-s', 'http://'+ip])
        output = santize(output)
    except Exception as e:
        return json.dumps([ip, e.message])

    return json.dumps( [ip, output.replace("\n", " ").replace("/r", '')])




def scan_ips(ip_set, outfname):
    start_t = time.time()
    pool = Pool(processes=max_proc)
    with open(outfname, 'w') as outf:
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


random.shuffle(ip_list)
scan_ips(ip_list, sys.argv[1]+'.scan.res')


#scan_ips(set(['52.200.189.78', '52.200.189.77', '34.225.47.67', '34.203.109.236', '52.54.211.81']))
# ip = '52.200.189.78'
# port = 80
# print port_open(ip, port )

# print curl_ip('52.200.189.77')
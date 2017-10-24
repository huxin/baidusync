#!/usr/bin/env python

# download files from baidu pan and compute md5 according to local file directories
# downloaded file will be removed after hash is computed

import os
import sys
import subprocess32
import time
import hashlib
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

if len(sys.argv) != 3:
    print "Usage:", sys.argv[0], "<local dir> <remote dir>"
    exit(1)

def load_history():
    history = set()
    for f in os.listdir('.'):
        if f.startswith('compare_result_'):
            print "Parsing result file:", f
            for l in  open(f, 'r'):
                p = l.strip().split()
                if len(p) == 0 or p[0] == -1:
                    continue
                local_file = p[-1]
                history.add(local_file)
    return history



def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

local_dir = sys.argv[1]
remote_dir = sys.argv[2]
tmp_download_file = 'tmp/download_file'

history = load_history()
print "already compared:", len(history), 'files'


if os.path.exists(tmp_download_file):
    os.unlink(tmp_download_file)

compare_res_file = 'compare_result_' + str(int(time.time()))

with open(compare_res_file, 'w') as res_file:
    for root, dirs, files in os.walk(local_dir):
        for f in files:
            local_full_path = os.path.join(root, f)
            remote_full_path = local_full_path.replace(local_dir, remote_dir)
            file_size = os.path.getsize(local_full_path)

            if local_full_path in history:
                print "Skip already parsed:", local_full_path
                continue
            # if file_size > 1000000:
            #     continue

            # download file
            print "\ndownloading:", remote_full_path
            cmd = ['bypy',  '-v',  '--select-fastest-mirror', '--downloader', 'aria2', 'downfile', remote_full_path, tmp_download_file]
            try:
                subprocess32.check_output(cmd, timeout=)
            except Exception as e:
                print "Download", remote_full_path, "failure", str(e)
                print >>res_file, '-1', local_full_path, remote_full_path
                continue

            # compute md5sum
            down_file_md5 = md5(tmp_download_file)
            local_file_md5 = md5(local_full_path)
            same = 0

            if down_file_md5 == local_file_md5:
                same = 1

            print >> res_file, same, down_file_md5, remote_full_path, local_file_md5, local_full_path
            print same, down_file_md5, remote_full_path, local_file_md5, local_full_path

            if os.path.exists(tmp_download_file):
                os.unlink(tmp_download_file)
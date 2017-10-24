#!/usr/bin/env python

# download files from baidu pan and compute md5 according to local file directories
# downloaded file will be removed after hash is computed

import os
import sys
import subprocess

if len(sys.argv) != 3:
    print "Usage:", sys.argv[0], "<local dir> <remote dir>"
    exit(1)

local_dir = sys.argv[1]
remote_dir = sys.argv[2]

for root, dirs, files in os.walk(local_dir):
    for f in files:
        local_full_path = os.path.join(root, f)
        remote_full_path = local_full_path.replace(local_dir, remote_dir)
        file_size = os.path.getsize(local_full_path)
        if file_size > 1000000:
            continue
        print local_full_path, remote_full_path, file_size


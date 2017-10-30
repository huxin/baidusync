# move verified upload (downloaded and uploaded) files to another directory
import os
import sys

if len(sys.argv) != 3:
    print "Usage:", sys.argv[0], "complete_res_file destination_dir"
    exit(1)

# don't delete .encfs6.xml

with open(sys.argv[1], 'r') as complete_file:
    for l in complete_file:
        l = l.strip()
        parts = l.split()
        if len(parts) > 0 and len(parts) != 4:
            print "Error line format:", l
            continue
        equal, md5, remote_path, local_md5, local_path = parts
        print equal, local_path
# move verified upload (downloaded and uploaded) files to another directory
import os
import sys

if len(sys.argv) != 3:
    print "Usage:", sys.argv[0], "complete_res_file destination_dir"
    exit(1)

# don't delete .encfs6.xml
base_dir = '/root/upload_data/'

with open(sys.argv[1], 'r') as complete_file:
    for l in complete_file:
        l = l.strip()
        parts = l.split()
        if len(parts) > 0 and len(parts) != 5:
            print "Error line format:", l
            continue
        equal, md5, remote_path, local_md5, local_path = parts
        if local_path.startswith(base_dir) == False:
            print "FATAL, localpath: ", local_path, 'not start with:', base_dir
            exit(1)

        print equal, local_path
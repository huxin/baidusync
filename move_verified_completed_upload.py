# move verified upload (downloaded and uploaded) files to another directory
import os
import sys

if len(sys.argv) != 3:
    print "Usage:", sys.argv[0], "complete_res_file destination_dir"
    exit(1)

with open(sys.argv[1], 'r') as complete_file:
    for l in complete_file:
        print l
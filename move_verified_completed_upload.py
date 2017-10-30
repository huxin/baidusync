# move verified upload (downloaded and uploaded) files to another directory
import os
import sys
import shutil

if len(sys.argv) != 3:
    print "Usage:", sys.argv[0], "complete_res_file destination_dir"
    exit(1)

# don't delete .encfs6.xml
base_dir = '/root/upload_data/'
dst_dir = sys.argv[2]

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

        if equal != '1' or md5 != local_md5:
            print "Skip not equal files:", local_path

        # once we verified that they are the same, we move them to new location
        # 1. replace base_dir with the new destination dir
        new_full_path = os.path.join(dst_dir, local_path.replace(base_dir, ''))
        print "move", local_path, "to", new_full_path
        filename = os.path.basename(new_full_path)
        new_dir = new_full_path.replace(filename, '')
        if os.path.exists(new_dir) == False:
            # create new_dir
            print "Creating:", new_dir
            os.makedirs(new_dir)

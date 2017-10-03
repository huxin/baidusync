import os
import sys
import hashlib

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def get_file_md5(d):
    file2md5 = {}
    for root, dirs, files in os.walk(d):
        for f in files:
            fullpath = os.path.join(root, f)
            # get md5
            file2md5[fullpath] = md5(fullpath)
    return file2md5


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print sys.argv[0], '<dir>'
        exit(1)

    root_dir = sys.argv[1]
    file2md5 = get_file_md5(root_dir)

    basename = os.path.basename(root_dir)
    if basename == '.':
        basename = 'files'

    with open(basename + '.md5', 'w') as outf:
        for f, md5 in file2md5.items():
            print >> outf, md5, f

    # for d in os.listdir(sys.argv[1]):
    #     if os.path.isdir(d):
    #         file2md5 = get_file_md5(d)
    #
    #         # output results
    #         with open(d+'.md5', 'w') as outf:


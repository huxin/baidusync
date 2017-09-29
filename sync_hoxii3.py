#!/usr/bin/env python
from tendo import singleton
import os
import time

# 0 0,12 * * * python /root/baidusync/sync_hoxii3.py

me = singleton.SingleInstance()

ts = "[{}]".format(time.ctime())
os.system("echo {} >> /var/log/baidusync/hoxii3.log".format(ts))
os.system("echo {} > /root/upload_data/hoxii3_upload_ts.txt".format(ts))
cmd = "/usr/local/bin/bypy -e -v syncup /root/upload_data Encrypt >> /var/log/baidusync/hoxii3.log 2>>/var/log/baidusync/hoxii3.err"
os.system(cmd)
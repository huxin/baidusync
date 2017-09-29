#!/usr/bin/env python
from tendo import singleton
import os
import time

# this should be run every 15 minutes

me = singleton.SingleInstance()

ts = "[{}]".format(time.ctime())
os.system("echo {} >> /var/log/hoxii2.log".format(ts))
os.system("echo {} >> /root/upload_data/hoxii2_upload_ts.txt".format(ts))
cmd = "/usr/local/bin/bypy -e -v syncup /root/upload_data enc >> /var/log/baidusync/hoxii2.log 2>>/var/log/baidusync/hoxii2.err"
os.system(cmd)
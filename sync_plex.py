#!/usr/bin/env python
from tendo import singleton
import os
import time

me = singleton.SingleInstance()


ts = "[{}]".format(time.ctime())
os.system("echo {} >> /var/log/plex.log".format(ts))
cmd = "/usr/local/bin/bypy -v --mirror allall01.baidupcs.com --downloader aria2 syncdown plex /root/plex True > /var/log/baidusync/plex.log 2>/var/log/baidusync/plex.err"
os.system(cmd)
#!/usr/bin/env python
from tendo import singleton
import os
import time

me = singleton.SingleInstance()


ts = "[{}]".format(time.ctime())
os.system("echo {} >> /var/log/baidusync/plex.log".format(ts))
cmd = "cd /root; /usr/local/bin/bypy -v  --select-fastest-mirror --downloader aria2 syncdown plex plex True >> /var/log/baidusync/plex.log 2>>/var/log/baidusync/plex.err"
os.system(cmd)
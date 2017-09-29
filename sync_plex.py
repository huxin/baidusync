from tendo import singleton
import os

me = singleton.SingleInstance()

cmd = "/usr/local/bin/bypy -v --downloader aria2 syncdown plex /root/plex True > /var/log/baidusync/plex.lg 2>/var/log/baidusync/plex.err"
os.system(cmd)
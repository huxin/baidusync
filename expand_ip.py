import ipaddress
import sys


if len(sys.argv) != 2:
    print sys.argv[0], "ip_file"
    exit(1)


expandf = open(sys.argv[1] + '.lst', 'w')
cnt = 0
for p in open(sys.argv[1]):
    p = p.strip()
    if p.find('.') == -1:
        continue
    # expand ip prefix
    cidr = ipaddress.ip_network(unicode(p))
    for ip in cidr:
        print >> expandf, ip
        cnt += 1

print "Total expanded ips: ", cnt
expandf.close()


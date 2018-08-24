import re
import os
domain_regex=re.compile(r'^[\w-]+(\.\w+)?\.\w+\.(com|cn|io|net|org)$')
iport_regex=re.compile('^((2[0-4][0-9]|25[0-5]|1[0-9][0-9]|[1-9]?[0-9])(\.(2[0-4][0-9]|25[0-5]|1[0-9][0-9]|[1-9]?[0-9])){3}|portainer)\:[1-9]\d{3,6}$')

def domain_status(domain):
    m=domain_regex.match(domain)
    if m:
        return "domainyes"
    else:
	return "domainno"
def iport_status(iport):
    regex = re.compile('\s+')
    iport_list=regex.split(iport)
    print iport_list
    l=len(iport)
    for i in range(l):
        im=iport_regex.match(iport_list[i])
        if im:
	    spt=int(im.group().split(':')[1])
	    if 20000 > spt > 8000:
		    return "iportyes"
	    else:
		   print "port limit err"
		   return "iportno"
        else:
	    return "iportno"

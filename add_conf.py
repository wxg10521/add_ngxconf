#-*- coding:utf-8 -*-
import os,re
ngxconf_dir='/nginx/conf.d'
#domain='www.baidu.com'
#iport='10.11.3.28:9999 10.11.3.22:3333 10.11.3.44:2222'
class add_conf():
    @staticmethod
    def cre_dir(domain):
	global proxy_name
	global d_file
        d_dir='-'.join(domain.split('.')[1:])
	proxy_name='-'.join(domain.split('.'))
	d_dir='%s/%s' % (ngxconf_dir,d_dir)
	d_file='%s/%s.conf' % (d_dir,proxy_name)
	if os.path.isfile(d_file):
	    return False
	else:
	    if not os.path.exists(d_dir):
            	os.mkdir(d_dir)
	    return True
    @staticmethod  
    def cre_conf(domain,iport):
	#proxy_name='-'.join(domain.split('.'))
        #d_dir='-'.join(domain.split('.')[1:])
        lines= []
	with open("ngx-add.example","r") as conf:
	    for line in conf:
		lines.append(line)
            conf.close()
	lines.insert(2,"	server_name %s;" % domain)
	lines.insert(7,"	proxy_pass  %s;" % proxy_name)	
	lines.insert(14,"upstream %s {" % proxy_name)
	regex = re.compile('\s+')
	iport_list=regex.split(iport)
	l=len(iport_list)
	for i in range(l):
	    lines.insert(16+i,"	server %s;\n" % iport_list[i-1])
	wfile=open('%s' % d_file,"w+")
	for ii in lines:
	    wfile.write(ii)
	wfile.close()

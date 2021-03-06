# -*- coding:utf-8 -*-
import web
import regex_form
import sys
import alidns
import socket
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)
from  add_conf import add_conf
urls = (    #定义路由，用户访问界面
    '/','Index',  #首页，首页指向
    '/(.*)', 'hello'
)
render = web.template.render('templates')
class hello:        
    def GET(self, www):
	form = web.input(name="",greet="")
        if form.greet!="" and form.name!="":
		name=str(form.name)
		pw=str(form.greet)
		if name == "admin":
			return 'hello  '+ www
		else:
			return 'error  ' + name
	else:
		return "please enter user"
class Index(object):
    def GET(self):
	form = web.input(domain="",iport="")
	domain=str(form.domain)
	iport=str(form.iport)
	domains=regex_form.domain_status(domain)
	iports=regex_form.iport_status(iport)
	domain_dir=domain.split()
        if domain!="" and iport!="":
		if domains == "domainyes" and iports == "iportyes":
		    if add_conf.cre_dir(domain):
			opfl=open('domainlist','a+')
			opfl.write('%s %s' % (domain,iport))
			opfl.write('\n')
			opfl.close()
		     	add_conf.cre_conf(domain,iport)
			dns_tld_list=domain.strip('.').split('.')[-2:]
			dns_tld='.'.join(dns_tld_list)
			if dns_tld == 'test.com': 
			    dns_pre_list=domain.strip('.').split('.')[:-2]
			    dns_pre='.'.join(dns_pre_list)
			    alidns.xiaoyun_dns_record('test.com',dns_pre)
			    return 'The configuration and DNS success :'+ domain +"  " + iport
			else:
			    return 'Configuration success,DNS not resolved !'+ domain +"  " + iport
		    else:
			dns_tld_list=domain.strip('.').split('.')[-2:]
                        dns_tld='.'.join(dns_tld_list)
                        if dns_tld == 'test.com':
			    hostip=socket.gethostbyname(domain)
			    if hostip != '103.249.254.8':
			        dns_pre_list=domain.strip('.').split('.')[:-2]
			        dns_pre='.'.join(dns_pre_list)
			        alidns.xiaoyun_dns_record('test.com',dns_pre)
			return 'Already exists configure '+ domain + iport
		else:
			return 'Unknom error ' + domain+ "  " + iport
        return render.index()
if __name__ == '__main__':
    web.application(urls,globals()).run()

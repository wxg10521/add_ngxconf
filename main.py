# -*- coding:utf-8 -*-
import web
import red
import sys
import alidns
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
	domains=red.domain_status(domain)
	iports=red.iport_status(iport)
	domain_dir=domain.split()
        if domain!="" and iport!="":
		if domains == "domainyes" and iports == "iportyes":
		    if add_conf.cre_dir(domain):
			opfl=open('domainlist','a+')
			opfl.write('%s %s' % (domain,iport))
			opfl.write('\n')
			opfl.close()
		     	add_conf.cre_conf(domain,iport)
			dns_pre_list=domain.strip('.').split('.')[:-2]
			dns_pre='.'.join(dns_pre_list)
			alidns.xiaoyun_dns_record('xiaoyun.com',dns_pre)
			return 'hello '+ domain +"  " + iport
		    else:
			dns_pre_list=domain.strip('.').split('.')[:-2]
			dns_pre='.'.join(dns_pre_list)
			alidns.xiaoyun_dns_record('xiaoyun.com',dns_pre)
			return 'already exists '+ domain + iport
		else:
			return 'error ' + domain+ "  " + iport
        return render.index()
if __name__ == '__main__':
    web.application(urls,globals()).run()

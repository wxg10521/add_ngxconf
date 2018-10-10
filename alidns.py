#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526 import StopInstanceRequest
from aliyunsdkalidns.request.v20150109 import DescribeDomainsRequest,DescribeDomainRecordsRequest,UpdateDomainRecordRequest,AddDomainRecordRequest,DeleteDomainRecordRequest,SetDomainRecordStatusRequest
import json,urllib,re
import sys

# 创建AcsClient实例
client = AcsClient(
   "access_keysId",
   "<accessSecret>",
   "regiond（cn-beijing）"
);

#获取二级域名
def list_domain():
    DomainList = DescribeDomainsRequest.DescribeDomainsRequest()
    DomainList.set_accept_format('json')
    DNSListJson = json.loads(client.do_action_with_exception(DomainList))
    for i in DNSListJson['Domains']['Domain']:
        print i['DomainName']
    #print DNSListJson
    
#获取域名信息（修改自己的DomainName）
def list_dns_record(DomainName):
    DomainRecords = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    DomainRecords.set_accept_format('json')
    DomainRecords.set_DomainName(DomainName)
    DomainRecordsJson = json.loads(client.do_action_with_exception(DomainRecords))
    print DomainName+':'
#    print DomainRecordsJson
    for x in DomainRecordsJson['DomainRecords']['Record']:
         RecordId = x['RecordId']
         RR = x['RR']
         Type = x['Type']
         Line = x['Line']
         Value = x['Value']
         TTL = x['TTL']
         Status = x['Status']
         txt =  RecordId+' '+RR+' '+Type+' '+Line+' '+Value+' '+str(TTL)+' '+Status
         print txt
    print '\n'
    

#更新域名解析（修改的域名DomainName，和要修改的hostname，修改成hostname_new，解析的类型Types，解析的地址IP）
def edit_dns_record(DomainName, hostname, hostname_new, Types, IP):
    DomainRecords = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    DomainRecords.set_accept_format('json')
    DomainRecords.set_DomainName(DomainName)
#   打印显示一页500条记录，最多500，默认20
    DomainRecords.add_query_param('PageSize', '500')
    DomainRecordsJson = json.loads(client.do_action_with_exception(DomainRecords))
#   打印页数
#    DomainRecords.add_query_param('PageSize', '2')
    for x in DomainRecordsJson['DomainRecords']['Record']:
        if hostname == x['RR']:
            RecordId = x['RecordId']
            UpdateDomainRecord = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
            UpdateDomainRecord.set_accept_format('json')
            UpdateDomainRecord.set_RecordId(RecordId)
            UpdateDomainRecord.set_RR(hostname_new)
            UpdateDomainRecord.set_Type(Types)
            UpdateDomainRecord.set_TTL('600')
            UpdateDomainRecord.set_Value(IP)
            UpdateDomainRecordJson = json.loads(client.do_action_with_exception(UpdateDomainRecord))
            print UpdateDomainRecordJson

#增加域名解析
def add_dns_record(DomainName, hostname, Types, IP):
    AddDomainRecord = AddDomainRecordRequest.AddDomainRecordRequest()
    AddDomainRecord.set_DomainName(DomainName)
    AddDomainRecord.set_RR(hostname)
    AddDomainRecord.set_Type(Types)
    AddDomainRecord.set_TTL('600')
    AddDomainRecord.set_Value(IP)
    AddDomainRecordJson = json.loads(client.do_action_with_exception(AddDomainRecord))
    print AddDomainRecordJson
    
#删除域名解析
def delete_dns_record(DomainName, hostname):
    DomainRecords = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    DomainRecords.set_accept_format('json')
    DomainRecords.set_DomainName(DomainName)
    DomainRecordsJson = json.loads(client.do_action_with_exception(DomainRecords))
    for x in DomainRecordsJson['DomainRecords']['Record']:
        if hostname == x['RR']:
            RecordId = x['RecordId']
            DeleteDomainRecord = DeleteDomainRecordRequest.DeleteDomainRecordRequest()
            DeleteDomainRecord.set_RecordId(RecordId)
            DeleteDomainRecordJson = json.loads(client.do_action_with_exception(DeleteDomainRecord))
            print DeleteDomainRecordJson

#设置域名解析
def set_dns_record(DomainName, hostname, status):
    DomainRecords = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    DomainRecords.set_accept_format('json')
    DomainRecords.set_DomainName(DomainName)
    DomainRecordsJson = json.loads(client.do_action_with_exception(DomainRecords))
    for x in DomainRecordsJson['DomainRecords']['Record']:
        if hostname == x['RR']:
                RecordId = x['RecordId']
                SetDomainRecord = SetDomainRecordStatusRequest.SetDomainRecordStatusRequest()
                SetDomainRecord.set_accept_format('json')
                SetDomainRecord.set_RecordId(RecordId)
                SetDomainRecord.set_Status(status)
                SetDomainRecordJson = json.loads(client.do_action_with_exception(SetDomainRecord))
                print SetDomainRecordJson

#验证状态添加
def xiaoyun_dns_record(DomainName,hostname):
    DomainRecords = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    DomainRecords.set_accept_format('json')
    DomainRecords.set_DomainName(DomainName)
    DomainRecords.add_query_param('PageSize', '500')
    DomainRecordsJson = json.loads(client.do_action_with_exception(DomainRecords))
    print DomainName+':'
#    print DomainRecordsJson
    ValueDic={}
    for x in DomainRecordsJson['DomainRecords']['Record']:
        RR = x['RR']
        Value = x['Value']
        RR=RR.encode('utf8')
	Value=Value.encode('utf8')
        ValueDic[RR]=Value
#    print ValueDic
    if hostname in ValueDic:
	if ValueDic[hostname] == 'new-ngx.test.com':
            print 'DNS %s.%s CNAME new-ngx.test.com record already exists.' % (hostname,DomainName)
	else:
	    edit_dns_record(DomainName,hostname,hostname,'CNAME','new-ngx.test.com')
	    print 'DNS %s.%s CNAME new-ngx.test.com  edit success!' % (hostname,DomainName)
    else:
	print 'DNS %s.%s CNAME new-ngx.test.com add success' % (hostname,DomainName)
	add_dns_record(DomainName,hostname,'CNAME','new-ngx.test.com') 
    print '\n'

DomainName = sys.argv
for i in DomainName:
    if i == sys.argv[0]:
        pass
    else:
        list_dns_record(i)
#xiaoyun_dns_record('test.com','20170315')
#edit_dns_record('test.com', 'admin', 'admin', 'CNAME', 'new-ngx.test.com')
#edit_dns_record('test.com', 'h5-demo1', 'h5-demo1', 'A', '103.249.2.10')
#edit_dns_record('waayz.cn', 'test', 'test', 'A', '103.249.2.10')
#add_dns_record('waayz.cn', 'test', 'A', '103.249.2.10')
#add_dns_record('waayz.cn', 'test_ok', 'A', '103.249.2.10')
#delete_dns_record('waayz.cn','test_ok')
#set_dns_record('waayz.cn', 'test_ok', 'DISABLE')
#set_dns_record('waayz.cn', 'test_ok', 'ENABLE')
#list_domain()

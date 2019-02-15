#!/usr/bin/env python
#coding:utf8

'''
Created on 03.06.2015
'''

import optparse
import sys
import traceback
import json
from getpass import getpass
from core import ZabbixAPI

def get_options():
    usage = "usage: %prog [options]"
    OptionParser = optparse.OptionParser
    parser = OptionParser(usage)

    parser.add_option("-s","--server",action="store",type="string",\
        dest="server",help="(REQUIRED)Zabbix Server URL.")
    parser.add_option("-u", "--username", action="store", type="string",\
        dest="username",help="(REQUIRED)Username (Will prompt if not given).")
    parser.add_option("-p", "--password", action="store", type="string",\
        dest="password",help="(REQUIRED)Password (Will prompt if not given).")
    parser.add_option("-H","--hostname",action="store",type="string",\
        dest="hostname",help="(REQUIRED)hostname for hosts.")
    parser.add_option("-k","--key",action="store",type="string",\
        dest="key",help="(REQUIRED)Item key.")
    parser.add_option("-n","--name",action="store",type="string",\
        dest="name",help="(REQUIRED)Name of the item.")
    parser.add_option("-T","--Template",action="store",type="string",\
        dest="template",help="(REQUIRED)templatename for template.")
    parser.add_option("-a","--application",action="store",type="string",\
        dest="application",default="",help="application name for template.")

    options,args = parser.parse_args()

    if not options.server:
        options.server = raw_input('server http:')

    if not options.username:
        options.username = raw_input('Username:')

    if not options.password:
        options.password = getpass()

    #if not options.hostname:
    #    options.hostname = raw_input('hostname:')

    return options, args

def errmsg(msg):
    sys.stderr.write(msg + "\n")
    sys.exit(-1)

if __name__ == "__main__":
    options, args = get_options()

    zapi = ZabbixAPI(options.server,options.username, options.password)

    hostname = options.hostname
    key = options.key
    name = options.name
    application=options.application

    if options.template:
      template = options.template
      template = zapi.template.get({"filter":{"host":template}})[0]
      templateid = template["templateid"]
      hostid = templateid
      _application = zapi.application.get({"output": "extend","templateids":hostid,"filter":{"name":application}})[0]
      applicationid = json.loads(json.dumps(_application))["applicationid"]
    else:
      hostid=zapi.host.get({"filter":{"host":hostname}})[0]["hostid"]
    #item=zapi.item.get({"output": "extend","hostids": hostid,"search":{"key_": key}})
    items =  zapi.item.get({"output": "extend","hostids": hostid,"search":{"key_": key}})
    for i in items:
      print i['itemid'],i['name'],i['key_']
    #print hostid,'\t',item

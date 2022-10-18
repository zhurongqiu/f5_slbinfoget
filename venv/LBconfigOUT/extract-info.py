#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests, json, ssl,xlwt
requests.packages.urllib3.disable_warnings()
ssl._create_default_https_context = ssl._create_unverified_context

bigip = requests.session()
bigip.auth = ('account', 'password')
bigip.verify = False
bigip.headers.update({'Content-Type' : 'application/json'})
ip = ('255.255.255.255')   #IP地址

#def VSname():
#    response = bigip.get(url='https://' + ip + '/mgmt/tm/ltm/virtual/', verify=False)
#    vsinfoall = json.loads(response.text)
#    vsinfo = vsinfoall['items']
#    for x in vsinfo:
#        vsname = x['name']
#        poolname = x['pool']
#        print('vsname:' + vsname)
#        print('poolname:' + poolname)

responsevs = bigip.get(url='https://'+ip+'/mgmt/tm/ltm/virtual/', verify=False)#从接口获取VS相关信息
print(responsevs)
vsinfoall = json.loads(responsevs.text)#将JSON格式转化为字典
vsinfo = vsinfoall['items']#提取vs信息
f = open('E://'+ip+'-config.txt','w')
#print(vsinfo)
for x in vsinfo:
    vsname = x['name']#vs名称
    poolname = x['pool']  #带/common/的POOL名称
    ipprotacol = x['ipProtocol']
    vsip = x['destination'][8:]
    pool_nocommon = poolname[8:]
    if ('persist') in x:
        persistinfo = x['persist'][0]
        persist = persistinfo['name']
    else:
        persist = 'null';
    responsepool = bigip.get(url='https://'+ ip + '/mgmt/tm/ltm/pool/~Common~'+pool_nocommon, verify=False)
    poolinfoall = json.loads(responsepool.text)
    LBcfg = poolinfoall['loadBalancingMode']
    responsemember = bigip.get(url='https://'+ ip + '/mgmt/tm/ltm/pool/~Common~'+pool_nocommon+'/members', verify=False)
    memberinfoall = json.loads(responsemember.text)
    memberinfo = memberinfoall['items']
    members = '/'.join(y['fullPath'][8:] for y in memberinfo)
#    for y in memberinfo:
#        member = y['address']
#        members =  (members ++ '/' + member)
#    print(LBcfg)
#    print('vsname:'+ vsname)
#    print('poolname:'+ poolname)
#    print(pool_nocommon)
    print(vsname + ' ' + vsip + ' ' + pool_nocommon + ' ' + ipprotacol+ ' ' + LBcfg + ' ' + members + ' ' + persist,file=f)
    members = ''
    persist = ''



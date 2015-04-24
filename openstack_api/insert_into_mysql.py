'''

@author: tianyuan8
'''
import sys
import MySQLdb
import string
from find_tenant import query_tenant
from find_flavor import query_flavor
from find_vms import query_vm
from find_router import query_routers
from find_tenant_quota import query_tenant_quota
VM_DETAIL = False
reload(sys)
USERNAME="admin"
PASSWORD = "admin123"
sys.setdefaultencoding( "utf-8" )

if len(sys.argv)>3:
    print "python find.py <ip > <tenant>"
    exit(0)
    
elif len(sys.argv)==3:
    ip = sys.argv[1]
    t = sys.argv[2]
elif sys.argv == 2:
    ip = sys.argv[1]
    t = ""
else:
    ip = "192.168.0.2"
    t = ""
    
    
t_id = ""
    
tenants = query_tenant(ip,USERNAME,PASSWORD)

if t:
    for one_t in tenants:
        if tenants[one_t]["name"] == t:
            t_id = one_t
            
flavors = query_flavor(ip,USERNAME,PASSWORD)
vms = query_vm(ip)

routers = query_routers(ip,USERNAME,PASSWORD)

sort_dict = {}
sort_routers = {}

for router in sort_routers:
    if router['id'] in sort_routers:
        sort_routers[router['id'] ] = sort_routers[router['id'] ] + 1
    else : 
        sort_routers[router['id'] ] = 1

for vm in vms:
    if vm["tenant_id"] not in sort_dict:
        sort_dict[vm["tenant_id"]] = [vm]
    else:
        sort_dict[vm["tenant_id"]].append(vm)
        
if t_id:
    sort_dict = {t_id:sort_dict[t_id]}

conn =   MySQLdb.connect(host="localhost",user="tianyuan",passwd="tianyuan",db="statistic",charset="utf8")        
cursor = conn.cursor()
delete_all = "delete from Tenant"      
cursor.execute(delete_all) 

tenant_num = 0       
for one in sort_dict:
    value = []
    tenant_num = tenant_num +1
    #print "TENANT_ID :    %s"%(one)
    value.append(one)
    if tenants.has_key(one):
        #print "TENANT_NAME :    %s"%(tenants[one]["name"])
        value.append(tenants[one]["name"])
    else:
        value.append('UNKNOWN')
        #print "TENANT_NAME :    %s"%("UNKNOWN")
        
    quota =   query_tenant_quota(ip, one ,USERNAME,PASSWORD)
    #print "VM COUNT :    %s/%s"%(len(sort_dict[one]),quota['instances'])
    value.append(len(sort_dict[one]))
    value.append(quota['instances'])
    ram = 0
    cpu = 0
    disk = 0
    for one_vm in sort_dict[one]:
        flavor_id = one_vm["flavor"]["id"]
        ram = ram + flavors[flavor_id]["ram"]
        cpu = cpu + flavors[flavor_id]["vcpus"]
        disk = disk + flavors[flavor_id]["disk"]
    value.append(cpu)
    value.append(quota['cores'])
    value.apend(ram)
    value.append(quota['ram'])
    value.append(disk)
    print value
    cursor.execute('insert into Tenant values(%s,%s,%s,%s,%s,%s,%s,%s,%s)',value)
    #print "VM CPU :    %s/%s"%(cpu,quota['cores'])
    #print "VM RAM :    %s/%s"%(ram,quota['ram'])
    #print "vm DISK:    %s"%(disk)
                     
    
    #print ""
    

    if VM_DETAIL:
        
        print "**************************************************************************************************************************"
    
        for one_vm in sort_dict[one]:
            print "---------------------------------------------------------------------------------"
            
            print "NAME:   "+ one_vm["name"]
            print "STATUS :" + one_vm['status']    
            flavor_id = one_vm["flavor"]["id"]
      
            print "RAM :    %s , CPU :    %s , DISK :    %s"%(flavors[flavor_id]["ram"],flavors[flavor_id]["vcpus"],flavors[flavor_id]["disk"])
            
            print "NETWORK : "
            
            print one_vm['addresses']
            
      
conn.commit()
cursor.close()
conn.close 
  

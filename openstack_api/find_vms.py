'''

@author: tianyuan8
'''

from utils import json_request



def _conn_keystone(ip,username="admin",password = "admin123",port = "5000"):
    '''
    curl -i 'http://192.168.0.2:5000/v2.0/tokens' -X POST -H "Accept: application/json" -H "Content-Type: application/json" -H "User-Agent: python-novaclient" -d '{"auth": {"tenantName": "admin", "passwordCredentials": {"username": "admin", "password": "admin123"}}}'
    return token id
    '''
    url =  "http://"+ip+":"+port+"/v2.0/tokens"
    data = {"auth": {"tenantName": "admin", "passwordCredentials": {"username": username, "password": password}}}
    headers = {'Content-Type': 'application/json','User-Agent': 'python-novaclient', 'Accept':"application/json"}
    result = json_request(url,'POST',data , headers)
    if not result.has_key("access"):
        raise Exception("get token error")
    return result["access"]



def _query_vm(result):
    '''
    curl -i 'http://10.120.16.100:8774/v2/42b779463dd4444eb5e575ea90e8a6b9/servers/detail?all_tenants=1' -X GET -H "Accept: application/json" -H "User-Agent: python-novaclient" -H "X-Auth-Project-Id: admin" -H "X-Auth-Token: dcf17d8942084972b13ec4504c95496a"
    '''

    data = {}
    url = ""
    token_id = result["token"]["id"]
    services = result["serviceCatalog"]
    for one in services:
        if one["name"] == "nova":
            endpoints_list = one["endpoints"]
            for endpoint in endpoints_list:
                if endpoint.has_key("publicURL"):
                    url = endpoint["publicURL"]+"/servers/detail?all_tenants=1"
    headers = {'X-Auth-Token': token_id, 'User-Agent': 'python-novaclient' , 'Accept':'application/json','X-Auth-Project-Id':'admin'}
    result = json_request(url,'GET',data , headers)
    if result.has_key("servers"):
        return result["servers"]
    
    else:
        raise Exception("query vm error")
  

def query_vm(ip,username="admin",password = "admin123"):
    

    result = _conn_keystone(ip,username="admin",password = "admin123")
    vms = _query_vm(result)
    return vms



'''
[{"status": "ACTIVE", 
 "updated": "2015-04-19T08:24:33Z",
 "hostId": "9cc3f6c72d329a885d6f5888debd3a38b981612999a8c87f40334701",
 "OS-EXT-SRV-ATTR:host": "node-8.domain.tld",
 "addresses": 
      {"share_net": [
                    {"OS-EXT-IPS-MAC:mac_addr": "fa:16:3e:df:41:e5", "version": 4, "addr": "192.168.111.17", "OS-EXT-IPS:type": "fixed"}, 
                    {"OS-EXT-IPS-MAC:mac_addr": "fa:16:3e:df:41:e5", "version": 4, "addr": "10.120.16.167", "OS-EXT-IPS:type": "floating"}
      },

 "links": [{"href": "http://10.120.16.100:8774/v2/42b779463dd4444eb5e575ea90e8a6b9/servers/6e78b692-43b0-46c8-85d6-d2429001b61a", "rel": "self"}, 
           {"href": "http://10.120.16.100:8774/42b779463dd4444eb5e575ea90e8a6b9/servers/6e78b692-43b0-46c8-85d6-d2429001b61a", "rel": "bookmark"}],

 "key_name": null, 

 "image": {"id": "7504e472-8432-4a34-9751-e27090bed199", 
           "links": [{"href": "http://10.120.16.100:8774/42b779463dd4444eb5e575ea90e8a6b9/images/7504e472-8432-4a34-9751-e27090bed199", "rel": "bookmark"}]}, 

  "OS-EXT-STS:task_state": null, 

  "OS-EXT-STS:vm_state": "active",

  "OS-EXT-SRV-ATTR:instance_name": "instance-0000004c",

  "OS-SRV-USG:launched_at": "2015-01-30T06:57:46.000000", 

  "OS-EXT-SRV-ATTR:hypervisor_hostname": "node-8.domain.tld", 

  "flavor": {"id": "64", "links": [{"href": "http://10.120.16.100:8774/42b779463dd4444eb5e575ea90e8a6b9/flavors/64", "rel": "bookmark"}]}, 

  "id": "6e78b692-43b0-46c8-85d6-d2429001b61a", 

  "security_groups": [{"name": "default"}],

  "OS-SRV-USG:terminated_at": null,
     
   "OS-EXT-AZ:availability_zone": "nova", 

   "user_id": "66109560592643a6843fb838b8018eba", 

   "name": "wso2dssdx01", 

   "created": "2015-01-22T14:47:18Z",

   "tenant_id": "c3c1717637424f929abc02dde85b090c",

   "OS-DCF:diskConfig": "MANUAL",

   "os-extended-volumes:volumes_attached": [],

   "accessIPv4": "", "accessIPv6": "", 

   "progress": 0, 

   "OS-EXT-STS:power_state": 1,

   "config_drive": "", "metadata": {}
},...]
'''

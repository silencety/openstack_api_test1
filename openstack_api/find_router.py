'''

@author: tianyuan8
'''



from utils import json_request

#endpoint = 'http://192.168.0.2:5000'

def _conn_keystone(ip,username="admin",password = "admin123",port = "5000"):
    '''
    curl -i http://192.168.0.2:5000/v2.0/tokens -X POST -H "Content-Type: application/json" -H "Accept: application/json" -H "User-Agent: python-neutronclient" -d '{"auth": {"tenantName": "admin", "passwordCredentials": {"username": "admin", "password": "admin123"}}}'
   
    return token id
    '''
    url =  "http://"+ip+":"+port+"/v2.0/tokens"
    data = {"auth": {"tenantName": "admin", "passwordCredentials": {"username": username, "password": password}}}
    headers = {'Content-Type': 'application/json','User-Agent': 'python-neutronclient','Accept': 'application/json'}
    result = json_request(url,'POST',data , headers)
    if not result.has_key("access"):
        raise Exception("get token error")
    return result["access"]




def _query_routers(result):
    '''
     curl -i http://10.120.16.100:9696/v2.0/routers.json -X GET -H "X-Auth-Token: c03da5a8386746879e238224831d9c4d" -H "Content-Type: application/json" -H "Accept: application/json" -H "User-Agent: python-neutronclient"
    '''

    data = {}
    url = ""
    token_id = result["token"]["id"]
    services = result["serviceCatalog"]
    for one in services:
        if one["name"] == "neutron":
            endpoints_list = one["endpoints"]
            for endpoint in endpoints_list:
                if endpoint.has_key("publicURL"):
                    url = endpoint["publicURL"]+"/v2.0/routers.json"
                    
    headers = {'X-Auth-Token': token_id, 'User-Agent': 'python-neutronclient' , 'Accept':'application/json','Content-Type': 'application/json'}
    
    result = json_request(url,'GET',data , headers)
    if result.has_key("routers"):
        return result["routers"]
    else:
        raise Exception("find router error")

   

def query_routers(ip,username="admin",password = "admin123"): 
    
    ret={}   

    result = _conn_keystone(ip,username="admin",password = "admin123")
    routers = _query_routers(result)
    for one in routers:
        ret[one['id']] = one
        
    return ret


'''
   [{
   u'status': u'ACTIVE',
   u'external_gateway_info': {u'network_id': u'c73dbb6c-ed8d-4d20-b218-d91c1d0d1de6', u'enable_snat': True, u'external_fixed_ips': [{u'subnet_id': u'26df3013-9633-4c42-a2a5-e90d65c75648', 
   u'ip_address': u'10.120.17.164'}]}, 
   u'portforwardings': [{u'inside_addr': u'10.120.17.162', u'protocol': u'tcp', u'outside_port': 22, u'inside_port': 22}], 
   u'name': u'CX101 Router',
   u'admin_state_up': True, 
   u'tenant_id': u'e6b0e512f4454f0d92ba81d04f09622c', 
   u'routes': [],
   u'id': u'48f88a88-d0a8-40f0-8367-af59b0a32e2a'
    },...]
'''
        
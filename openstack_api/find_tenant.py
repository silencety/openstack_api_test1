
from utils import json_request

#endpoint = 'http://192.168.0.2:5000'

def _conn_keystone(ip,port = "5000"):
    '''
    curl -i -X POST http://192.168.0.2:5000/v2.0/tokens -H "Content-Type: application/json" -H "User-Agent: python-keystoneclient" -d '{"auth": {"tenantName": "admin", "passwordCredentials": {"username": "admin", "password": "admin123"}}}'
    
    return token id
    '''
    url =  "http://"+ip+":"+port+"/v2.0/tokens"
    data = {"auth": {"tenantName": "admin", "passwordCredentials": {"username": "admin", "password": "admin123"}}}
    headers = {'Content-Type': 'application/json','User-Agent': 'python-keystoneclient'}
    result = json_request(url,'POST',data , headers)
    if not result.has_key("access"):
        raise Exception("get token error")
    return result["access"]



def _query_tenant(result):
    '''
    curl -i -X GET http://192.168.0.2:35357/v2.0/tenants -H "User-Agent: python-keystoneclient" -H "X-Auth-Token: 5077f9e5326a457ba5c7c3fa9873c066"
    
    '''

    data = {}
    url = ""
    token_id = result["token"]["id"]
    services = result["serviceCatalog"]
    for one in services:
        if one["name"] == "keystone":
            endpoints_list = one["endpoints"]
            for endpoint in endpoints_list:
                if endpoint.has_key("adminURL"):
                    url = endpoint["adminURL"]+"/tenants"
    headers = {'X-Auth-Token': token_id,'User-Agent': 'python-keystoneclient'}
    result = json_request(url,'GET',data , headers)
    tenants = []
    try:
        tenants = result["tenants"]
    except:
        pass
    return tenants

    
def query_tenant(ip):
    ret = {}
    result = _conn_keystone(ip)
    tenants = _query_tenant(result)
    for one in tenants:
        ret[one['id']]=one
    return ret
 



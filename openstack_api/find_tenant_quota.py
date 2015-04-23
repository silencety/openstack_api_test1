'''

@author: tianyuan8
'''

from utils import json_request

#endpoint = 'http://192.168.0.2:5000'

def _conn_keystone(ip,port = "5000"):
    '''
    curl -i 'http://192.168.0.2:5000/v2.0/tokens' -X POST -H "Accept: application/json" -H "Content-Type: application/json" -H "User-Agent: python-novaclient" -d '{"auth": {"tenantName": "admin", "passwordCredentials": {"username": "admin", "password": "admin123"}}}'
    
    return token id
    '''
    url =  "http://"+ip+":"+port+"/v2.0/tokens"
    data = {"auth": {"tenantName": "admin", "passwordCredentials": {"username": "admin", "password": "admin123"}}}
    headers = {'Content-Type': 'application/json','User-Agent': 'python-novaclient','Accept': 'application/json'}
    result = json_request(url,'POST',data , headers)
    if not result.has_key("access"):
        raise Exception("get token error")
    return result["access"]



def _query_tenant_quoto(result,tenant_id):
    '''
    curl -i 'http://10.120.16.100:8774/v2/42b779463dd4444eb5e575ea90e8a6b9/os-quota-sets/e6b0e512f4454f0d92ba81d04f09622c' -X GET -H "Accept: application/json" -H "User-Agent: python-novaclient" -H "X-Auth-Project-Id: admin" -H "X-Auth-Token: {SHA1}1f0cb32237c10a3ec36157036308a13777c33692"
    
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
                    url = endpoint["publicURL"]+"/os-quota-sets/"+str(tenant_id)
    headers = {'X-Auth-Token': token_id,'User-Agent': 'python-novaclient','Accept': 'application/json'}
    result = json_request(url,'GET',data , headers)
    '''
    result : 
    {"quota_set":
                {
                 "injected_file_content_bytes": 10240, 
                 "metadata_items": 1024,
                 "ram": 71200,
                 "floating_ips": 100, 
                 "key_pairs": 10, 
                 "id": "e6b0e512f4454f0d92ba81d04f09622c",
                 "instances": 100, 
                 "security_group_rules": 20,
                 "injected_files": 5, 
                 "cores": 300, 
                 "fixed_ips": -1, 
                 "injected_file_path_bytes": 255, 
                 "security_groups": 10}}
    '''
    quota = {}
    try:
        quota = result["quota_set"]
    except:
        pass
    return quota

    
def query_tenant_quota(ip,tenant_id):
    result = _conn_keystone(ip)
    quota = _query_tenant_quoto(result,tenant_id)
    return quota
 



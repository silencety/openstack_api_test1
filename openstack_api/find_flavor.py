'''

@author: tianyuan8
'''



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




def _query_flavor(result):
    '''
     curl -i 'http://10.120.16.100:8774/v2/42b779463dd4444eb5e575ea90e8a6b9/flavors/detail' -X GET -H "Accept: application/json" -H "User-Agent: python-novaclient" -H "X-Auth-Project-Id: admin" -H "X-Auth-Token: {SHA1}b625f16ede3e81b6bd3492b6e9d64648e241232a"
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
                    url = endpoint["publicURL"]+"/flavors/detail"
                    
    headers = {'X-Auth-Token': token_id, 'User-Agent': 'python-novaclient' , 'Accept':'application/json','X-Auth-Project-Id':'admin'}
    result = json_request(url,'GET',data , headers)
    if result.has_key("flavors"):
        return result["flavors"]
    else:
        raise Exception("find flavor error")

   

def query_flavor(ip): 
    
    ret={}   

    result = _conn_keystone(ip)
    flavors = _query_flavor(result)
    for one in flavors:
        ret[one['id']] = one
        
    return ret
        
 




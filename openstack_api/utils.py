import sys
import traceback


try:
    import json
except ImportError:
    import simplejson as json

import socket
from httplib import HTTPConnection, HTTPException
from urlparse import urljoin, urlparse
from sys import version_info
cookie = None
def json_request(url , method, data, headers):
    global cookie

    print url
    parts = urlparse(url)
    if cookie:
        headers['Cookie'] = cookie;
    if data:
        data = json.dumps(data)
    print data
    kwargs = {}
    if version_info[1] < 6:
        socket.setdefaulttimeout(30)
    else:
        kwargs['timeout'] = 30
    conn = HTTPConnection(parts.hostname, parts.port, **kwargs)
    try:
        conn.request(method, url, data, headers)
        response = conn.getresponse()
        data = response.read()
        #print data
        conn.close()
    except (socket.error, HTTPException), e:
        traceback.print_exc()
        return False

    if version_info[1] < 6:
        socket.setdefaulttimeout(None)

    if response.status > 299:
       
        if response.status == 401 and 'license' in data:
            print "error"
        else:
            print "error"
        return False
    cookie = response.getheader('Set-Cookie', cookie)
    # print cookie
    return data and json.loads(data) or True

#!/usr/bin/python

import urllib3
import thread

# URL = 'http://httpbin.org:80/ip'
URL = 'http://192.168.24.33:32420/icpIIBtest'

http = urllib3.PoolManager(num_pools=10)
# http = urllib3.HTTPConnectionPool('httpbin.org', port=80, maxsize=5)
print("Running HTTP stress test on IIB ...")


def http_request(http):
    while True:
        try:
            http.request('GET', URL)
        except Exception as e:
            print e


for t in range(0, 100):
    thread.start_new_thread(http_request, (http,))

# main program loop
while True:
    pass

#!/usr/bin/python

import urllib3
import thread
import sys
import socket

if len(sys.argv) != 3:
	print ("Usage: iib_stress_test.py <ip/hostname> <port>")
	sys.exit(1)

# try:
# 	socket.gethostbyname(sys.argv[1])
# except socket.gaierror as e:
# 	print (e)
# 	sys.exit(1)

try:
	socket.gethostbyname(sys.argv[1])
	if int(sys.argv[2]) < 0 or int(sys.argv[2]) > 65535:
		raise ValueError("Invalid port number")
except Exception as e:
	print (e)
	sys.exit(1)

# URL = 'http://httpbin.org:80/ip'
# URL = 'http://192.168.24.33:32420/icpIIBtest'
URL = 'http://' + sys.argv[1] + ':' + sys.argv[2] + '/hello'
print URL

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

#!/usr/bin/python

import urllib2
import urlparse
import thread, threading
import sys
import socket
import time

# try:
# 	socket.gethostbyname(sys.argv[1])
# except socket.gaierror as e:
# 	print (e)
# 	sys.exit(1)

URL = sys.argv[1]
o = urlparse.urlparse(URL)
IP = socket.gethostbyname(o.hostname)
URL = urlparse.urlunsplit((o.scheme, IP+':'+str(o.port or ''), o.path, o.query, o.fragment))

print "Running HTTP stress test on ", URL

# global thread-safe transaction counters
trans_counter = failed_counter = 0
threadLock = threading.Lock()

def http_request(param):
    global trans_counter
    global failed_counter

    while True:
        try:
            # https://stackoverflow.com/questions/35088139/how-to-make-a-thread-safe-global-counter-in-python/35088370
            with threadLock:
                trans_counter += 1
            response = urllib2.urlopen(URL+'?'+str(time.time()))
            if response.code <> 200:
                raise Exception()
        except Exception as e:
            # print e
            with threadLock:
                failed_counter += 1
            #time.sleep(1)

for t in range(0, 20):
    param = ''
    thread.start_new_thread(http_request, (param,))

# main program loop
trans_last = failed_last = 0
last = time.time()
while True:
    if time.time() - last > 1:
        print trans_counter-trans_last, failed_counter-failed_last
        trans_last, failed_last = trans_counter, failed_counter
        last = time.time()
    pass

# IIB on ICP Demo

## TODO:

- port forwards for separate iib instances
- MQ
- catalog item for demo chart



## Tests

1. HTTP GET single test:

	curl -s 192.168.24.33:32420/icpIIBtest

2. HTTP GET smoke test:

	curl -s 192.168.24.33:32420/icpIIBtest?[1-1000000] > /dev/null
    ... repeat for parallel TCP sessions



**Catch HTTP GETs**

	tcpdump -i calie423707f83c 'tcp[((tcp[12:1] & 0xf0) >> 2):4] = 0x47455420 and tcp port 4414'

**Monitor pods load in ICP**
	
	watch -n 1 kubectl top pod -l app=ibm-integration-bus-prod -n default

**Monitor message stats in iib**

TODO

## Links
IIB chart repo:
https://github.com/ot4i/iib-helm

IIB docker repo:
https://github.com/ot4i/iib-docker

https://developer.ibm.com/integration/blog/2017/09/18/lightweight-integration-useful-links/
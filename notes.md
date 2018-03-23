# IIB on ICP

Original git repo:

https://github.com/ot4i/iib-helm

## TODO:

- port forward
- curl session
- MQ
- catalog helm chart (rename experimental)

---


## Links

https://github.com/ot4i/iib-docker
https://developer.ibm.com/integration/blog/2017/09/18/lightweight-integration-useful-links/

## Tests

single test:

	curl -s 192.168.24.33:32420/icpIIBtest

smoke test:

	curl -s 192.168.24.33:32420/icpIIBtest?[1-1000000] > /dev/null

## Catch HTTP GET 

	tcpdump -i calie423707f83c 'tcp[((tcp[12:1] & 0xf0) >> 2):4] = 0x47455420 and tcp port 4414'

## Monitor pods load
	
	watch -n 1 kubectl top pod -l app=ibm-integration-bus-prod -n default

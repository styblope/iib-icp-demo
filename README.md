# IIB on IBM Cloud Private Demo

The following scenarios are covered:

1. IIB autoscaling and load balancing
2. IIB high-availablity
3. MQ integration

## TODO:

- port forwards for separate iib instances
- MQ
- catalog item for demo chart


## 1. Autoscaling with load balancer

Scalable IIB deployment is configured with cluster-wide NFS persistent volume (`/export/BARs`) which holds BARs files. Autoscaling is set based on CPU threshold (20%). Initial deployment starts one IIB instance and scales to two instances on high load. 

     kubectl autoscale deployment --max=2 --min=1 --cpu-percent=20 ibm-integration-bus-demo

The test scenario involves high volume injections of REST GET queries to the service until automatic instance scale-up gets triggered.

![](images/IIB-single.svg)
![](images/IIB.svg)

### Tests

**HTTP GET single test:**

	curl -s 192.168.24.33:32420/icpIIBtest

**HTTP GET smoke test:**

	curl -s 192.168.24.33:32420/icpIIBtest?[1-1000000] > /dev/null
    ... repeat for parallel TCP sessions

or better using the stress load script (which runs 100 parallel TCP connections)
    
    ./iib_stress_test.py


Monitor pods load in ICP
	
	watch -n 1 kubectl top pod -l app=ibm-integration-bus-prod -n default


Monitor message stats in iib instances

    kubectl port-forward <iib pod 1> 5000:4414
    kubectl port-forward <iib pod 2> 5001:4414

    and then from browser host:
    ssh -L 5000:localhost:5000 -L 5001:localhost:5001 master
    point browser to http://localhost:5000 and 5001


## 2. High availability

IIB high availability is configured using the pod Readiness and Liveness probes which check the IIB HTTP endpoint (exposed on TCP port 7800).

Test scenario involves blocking the port temporarily on one IIB pod instance and observing how kubernetes a) initially re-routes the incoming traffic and b) later restarts the pod.

### Tests

**Stop IIB node without killing pod**

    kubectl exec <iib pod name> -ti -- /opt/ibm/iib-10.0.0.10/server/bin/mqsistop IIB_NODE


<!-- Block incoming port using IPtables:

    kubectl exec <iib pod> -- /sbin/iptables -A INPUT -p tcp --destination-port 7800 -j DROP -->

Watch pod events

    watch "kubectl describe pods ibm-integration-bus-prod-686b58999d-fvdjq | tail"

Watch iib pods

    watch kubectl get pods -o wide -l app=ibm-integration-bus-prod
---

## Links
IIB chart repo:
https://github.com/ot4i/iib-helm

IIB docker repo:
https://github.com/ot4i/iib-docker

https://developer.ibm.com/integration/blog/2017/09/18/lightweight-integration-useful-links/
# Multi-node IIB with embedded global cache feature (eXtreme Scale)

Based on iib image from **ot4i/iib-docker** git repo:

	https://github.com/ot4i/iib-docker

## Building and running the container

Build the images in the ICP registry

    cd iib-docker
    docker build -t mycluster.icp:8500/default/iibv10image:globalcache .

Running standalone container with `default` cache policy

    docker run -d --rm --name iib-globalcache -e LICENSE=accept -e NODENAME=MYNODE -e SERVERNAME=MYSERVER -P -e CACHE_POLICY=default mycluster.icp:8500/default/iibv10image:globalcache

Verify that cache is running

    docker exec -ti iib-globalcache /bin/bash

    cd /opt/ibm/iib-10.0.0.11/server/bin
    source ./mqsiprofile
    ./mqsireportproperties MYNODE -b cachemanager -o CacheManager -r 2800-2819

## Push container to local registry

    docker push mycluster.icp:8500/default/iibv10image:globalcache

## Deploy iib replicas in k8s as StatefulSet

    kubects apply -f iib-service.yaml
    kubectl apply -f iib-statefulset.yaml

We'll use 2 replicas with embedded global cache on each node, running in HA mode.

## Configure multi-integration node cache topology

**Cache policy file**

> To share data across integration nodes, or enhance the availability of the cache, you must create a policy file. The policy file is an XML file that the cache manager uses to connect the caches of multiple integration nodes. Set the cache policy to the fully qualified name of the policy file.

Sample policy files are located here:

    cd /opt/ibm/iib-10.0.0.11/server/sample/globalcache

Customize `policy_two_brokers_ha.xml` by changing FQDN names (`hostname -f`) of the nodes and port ranges.

Create configmap with sample 2 brokers policy XML file

    kubectl create configmap iib-globalcache-policy --from-file=globalcache_policy.xml=policy_two_brokers_ha.xml

Modify the policy file so that it uses 3 brokers and splits the cache continers evenly among all three nodes while using the first 2 nodes as catalog servers. Scale up the iib statefulset to 3 replicas.

     kubectl create configmap iib-globalcache-policy --from-file=globalcache_policy.xml=policy_three_brokers_ha.xml

     kubectl scale statefulset iib-globalcache --replicas=3

## Verify cache placement

    kubectl exec -ti iib-globalcache-0 -- bash -c "mqsicacheadmin IIB_NODE -c showPlacement"

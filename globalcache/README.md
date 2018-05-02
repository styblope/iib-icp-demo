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

## Configure multi-integration node cache topology

**Cache policy file**

> To share data across integration nodes, or enhance the availability of the cache, you must create a policy file. The policy file is an XML file that the cache manager uses to connect the caches of multiple integration nodes. Set the cache policy to the fully qualified name of the policy file.

Sample policy files are located here:

    cd /opt/ibm/iib-10.0.0.11/server/sample/globalcache

Customize `policy_two_brokers_ha.xml` by changing FQDN names (`hostname -f`) of the nodes and port ranges.

In k8s, you may create a configmap with sample 2 brokers policy XML file like this:

    kubectl create configmap iib-globalcache-policy --from-file=globalcache_policy.xml=policy_two_brokers_ha.xml

## Verify cache placement

    kubectl exec -ti iib-globalcache-0 -- bash -c "mqsicacheadmin IIB_NODE -c showPlacement"

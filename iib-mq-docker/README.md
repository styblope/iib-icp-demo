# Origin

this repository is a merge of the original ot4i/iibdocker and ibm-messaging/mq-docker repositories on github

# Overview

This repository contains a Dockerfile and some scripts which demonstrate a way in which you might run [IBM Integration Bus](http://www-03.ibm.com/software/products/en/ibm-integration-bus) and IBM MQ in a [Docker](https://www.docker.com/whatisdocker/) container.

IBM would [welcome feedback](#issues-and-contributions) on what is offered here.

# Building the image

The image can be built using standard [Docker commands](https://docs.docker.com/userguide/dockerimages/) against the supplied Dockerfile.  For example:

~~~
cd iib-mq-docker
docker build -t iibv10image .
~~~

This will create an image called iibv10image in your local docker registry.

# What the image contains

The built image contains a full installation of [IBM Integration Bus for Developers Edition V10.0](https://ibm.biz/iibdevedn) and installation of [IBM MQ Advanced for Developers version 9.0.3]().

# Running a container

After building a Docker image from the supplied files, you can [run a container](https://docs.docker.com/userguide/usingdocker/) which will create and start an Integration Node to which you can [deploy](http://www-01.ibm.com/support/knowledgecenter/SSMKHH_10.0.0/com.ibm.etools.mft.doc/af03890_.htm) integration solutions.

In order to run a container from this image, it is necessary to accept the terms of the IBM Integration Bus for Developers license.  This is achieved by specifying the environment variable `LICENSE` equal to `accept` when running the image.  You can also view the license terms by setting this variable to `view`. Failure to set the variable will result in the termination of the container with a usage statement.  You can view the license in a different language by also setting the `LANG` environment variable.

In addition to accepting the license, you can optionally specify an Integration Node name using the `NODE_NAME` environment variable and an Integration Server name using the `SERVER_NAME` environment variable.

The last important point of configuration when running a container from this image, is port mapping.  The Dockerfile exposes ports `4414` and `7800` for IIB and `1414` and `9883` for MQ by default, for Integration Node administration and Integration Server HTTP traffic respectively.  This means you can run with the `-P` flag to auto map these ports to ports on your host.  Alternatively you can use `-p` to expose and map any ports of your choice.

For example:

~~~
docker run --name myNode -e LICENSE=accept -e NODE_NAME=MYNODE -P iibv10image -e MQ_QMGR_NAME=MQ1
~~~

If you wish, you can also deploy an IBM Integration Bus BAR files by mounting  a [Docker volume](https://docs.docker.com/engine/admin/volumes/volumes/) which makes the BAR file(s) available in `/tmp/BARs` directory in the container after it is started:
~~~
docker run --name myNode -v  /local/path/to/BARs:/tmp/BARs/<yourbars> -e LICENSE=accept -e NODE_NAME=MYNODE -e SERVER_NAME=MYSERVER -P iibv10image 
~~~

This will run a container that creates and starts an Integration Node called `MYNODE` and exposes ports `4414` and `7800` on random ports on the host machine. It also creates a queue manager called `MQ1` and starts this queue manager with some default queues defined.
For more information on configuring MQ please see [README.md](https://github.com/ibm-messaging/mq-docker/blob/master/README.md) for the standalone MQ container.

At this point you can use:
~~~
docker port <container name>
~~~

to see which ports have been mapped then connect to the Node's web user interface as normal (see [verification](# Verifying your container is running correctly) section below).

## Enabling embedded global cache
You can also enable the embedded eXtreme Scale global cache feature by specifying the `CACHE_POLICY` environment variable. The parameter specifies the policy to use for the cache manager. You can set this parameter to `default`, `disabled`, `none`, or the fully qualified name of an XML policy file. The default setting is `disabled`.

You can optionally specify `CACHE_PORT_RANGE` to define the range of ports that the cache manager can use. Set this parameter to `generate` (default) or to a specific range of ports. If you specify a range of ports, the value of this parameter must be in the format `xxxx-yyyy`, and the range must contain at least 20 ports

### Configure k8s multi-integration node cache topology

**Cache policy file**

> To share data across integration nodes, or enhance the availability of the cache, you must create a policy file. The policy file is an XML file that the cache manager uses to connect the caches of multiple integration nodes. Set the cache policy to the fully qualified name of the policy file.

Sample policy files are located here:

    cd /opt/ibm/iib-10.0.0.10/server/sample/globalcache

Customize `policy_two_brokers_ha.xml` by changing FQDN names (`hostname -f`) of the nodes and port ranges.

In k8s, create a configmap with sample 2 brokers policy XML file

    kubectl create configmap iib-globalcache-policy --from-file=globalcache_policy.xml=policy_two_brokers_ha.xml

You may modify the policy file so that it uses 3 brokers and splits the cache continers evenly among all three nodes while using the first 2 nodes as catalog servers. Scale up the iib statefulset to 3 replicas.

     kubectl create configmap iib-globalcache-policy --from-file=globalcache_policy.xml=policy_three_brokers_ha.xml

Verify cache placement

    kubectl exec -ti iib-globalcache-0 -- bash -c "mqsicacheadmin IIB_NODE -c showPlacement"

## Accessing logs

This image also configures syslog, so when you run a container, your node will be outputting messages to /var/log/syslog inside the container.  You can access this by attaching a bash session as described above or by using docker exec.  For example:

~~~
docker exec <container id> tail -f /var/log/syslog
~~~

# Verifying your container is running correctly

Whether you are using the image as provided or if you have customized it, here are a few basic steps that will give you confidence your image has been created properly:

1. Run a container, making sure to expose port 4414, 1414 and 9443 to the host - the container should start without error
2. Run mqsilist to show the status of your node as described above - your node should be listed as running
3. Access syslog as descried above - there should be no errors
4. Connect a browser to your host on the port you exposed in step 1 - the Integration Bus web user interface should be displayed.
5. Connect to a browser and connect via HTTPS to port 9443 to run the MQ administration console.

At this point, your container is running and you can [deploy](http://www-01.ibm.com/support/knowledgecenter/SSMKHH_10.0.0/com.ibm.etools.mft.doc/af03890_.htm) integration solutions to it using any of the supported methods.

# List of all Environment variables supported by this image

* **LICENSE** - Set this to `accept` to agree to the MQ Advanced for Developers license. If you wish to see the license you can set this to `view`.
* **LANG** - Set this to the language you would like the license to be printed in.
* **NODE_NAME** - Set this to the name you want your Integration Node to be created with.
* **SERVER_NAME** - Set this to the name you want your Integration Server to be created with.
* **CACHE_POLICY** - Set this to configure the embedded global cache. The parameter specifies the policy to use for the cache manager. You can set this parameter to `default`, `disabled`, `none`, or the fully qualified name of an XML policy file. 
* **CACHE_PORT_RANGE** - Specify the range of ports that the cache manager can use. Set this parameter to `generate` or to a specific range of ports. If you specify a range of ports, the value of this parameter must be in the format `xxxx-yyyy`, and the range must contain at least 20 ports

# License

The Dockerfile and associated scripts are licensed under the [Eclipse Public License 1.0](./LICENSE). IBM Integration Bus for Developers is licensed under the IBM International License Agreement for Non-Warranted Programs. This license may be viewed from the image using the `LICENSE=view` environment variable as described above. Note that this license does not permit further distribution.


IBM MQ Advanced for Developers is licensed under the IBM International License Agreement for Non-Warranted Programs. This license may be viewed from the image using the LICENSE=view environment variable as described above or may be found online. Note that this license does not permit further distribution.

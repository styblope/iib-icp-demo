# MQ TCP port ingress

Exposing TCP and UDP services:

https://github.com/kubernetes/ingress-nginx/blob/master/docs/user-guide/exposing-tcp-udp-services.md

https://www.nginx.com/blog/tcp-load-balancing-udp-load-balancing-nginx-tips-tricks/

https://github.com/kubernetes/ingress-nginx

Create configmap

    kubectl apply -n kube-system -f configmap.yaml

Modify nginx controller

    kubectl -n kube-system edit ds nginx-ingress-lb-amd64

Add `--tcp-services-configmap` argument

    spec:
      containers:
      - args:
        - /nginx-ingress-controller
        - --default-backend-service=$(POD_NAMESPACE)/default-http-backend
        - --configmap=$(POD_NAMESPACE)/nginx-load-balancer-conf
        - --tcp-services-configmap=$(POD_NAMESPACE)/nginx-ingress-controller-tcp


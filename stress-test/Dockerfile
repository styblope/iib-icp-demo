FROM ibmcom/icp-inception:2.1.0.3-ee

ADD iib_stress_test.py /

# Disable python output buffering python (python -u option)
ENV PYTHONUNBUFFERED=0

WORKDIR /

ENTRYPOINT ["/iib_stress_test_urllib2.py"]
CMD ["http://iib-loadbalancer.default.svc.cluster.local:7800/icpIIBtest"]

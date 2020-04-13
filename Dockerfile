FROM python:3.7-alpine
LABEL git_repo=https://github.com/reddi1979s/macaddresslookup_api_py_client

COPY macaddresslookup.py /tmp/macaddresslookup/
COPY docker_helper.sh /tmp/docker_helper.sh

ARG MACADDRESSIO_API_KEY
ENV MACADDRESSIO_API_KEY ${MACADDRESSIO_API_KEY}

ENV PATH $PATH:/tmp/macaddresslookup/

WORKDIR /tmp/macaddresslookup/
CMD [ "/bin/sh", "/tmp/docker_helper.sh" ]
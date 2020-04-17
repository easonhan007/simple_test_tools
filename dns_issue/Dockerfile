FROM ubuntu

RUN apt-get update && \
    apt-get install -y dnsutils net-tools iproute2 inetutils-ping curl dnsmasq && \
    apt-get clean

ADD empty.sh ./empty.sh


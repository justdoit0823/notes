
FROM debian:stretch

LABEL maintainer="justdoit920823@gmail.com"

RUN DEBIAN_RELEASE=stretch && \
    # Adding non-free repo for netperf
    echo "deb http://deb.debian.org/debian ${DEBIAN_RELEASE} non-free" > \
        /etc/apt/sources.list.d/debian-non-free.list && \
    apt-get -qq update && \
    apt-get -y install pbuilder aptitude linux-headers-4.9.0

RUN git clone https://github.com/iovisor/bcc.git /root/bcc

WORKDIR /root/bcc

RUN /usr/lib/pbuilder/pbuilder-satisfydepends && /root/bcc/scripts/build-deb.sh && dpkg -i *bcc*.deb

RUN mv /lib/modules/4.9.0-8-amd64 /lib/modules/$(uname -r) && rm -f *bcc*.deb

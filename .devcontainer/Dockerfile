FROM alpine:3.17

ENV MARIADB_USER=root
ENV MARIADB_PASSWORD=root
ENV LANG=zh_CN.UTF-8
ENV LANGUAGE=zh_CN.UTF-8

VOLUME [ "/sys/fs/cgroup", "/var/lib/mysql" ]

RUN sed -i 's@dl-cdn.alpinelinux.org@mirrors.aliyun.com@g' /etc/apk/repositories
RUN apk update
RUN apk add dumb-init \ 
    git \
    vim \
    wget \
    curl \
    openssl \
    openssl-dev \
    gcc \
    g++ \
    libffi-dev \
    make \
    zlib-dev \
    libcec-dev \
    libtool

## openrc
RUN apk add openrc
RUN mkdir -p /run/openrc \
    && touch /run/openrc/softlevel

## Mariadb
RUN apk add mariadb=10.6.12-r0 \
    mariadb-client=10.6.12-r0
RUN /etc/init.d/mariadb setup

## python3
RUN apk add python3 \
    python3-dev \
    jq \
    py3-configobj \
    py3-setuptools
RUN mkdir -p ~/.pip \
    && touch ~/.pip/pip.conf \
    && echo "[global]" >> ~/.pip/pip.conf \
    && echo "index-url = http://mirrors.aliyun.com/pypi/simple" >> ~/.pip/pip.conf \
    && echo "[install]" >> ~/.pip/pip.conf \
    && echo "trusted-host=mirrors.aliyun.com" >> ~/.pip/pip.conf
RUN wget https://bootstrap.pypa.io/get-pip.py \
    && python3 get-pip.py



EXPOSE 3306
EXPOSE 5959

CMD ["sh", "-c", "rc-service mariadb start"]
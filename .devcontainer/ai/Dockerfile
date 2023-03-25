FROM alpine:3.17

RUN sed -i 's@dl-cdn.alpinelinux.org@mirrors.aliyun.com@g' /etc/apk/repositories \
    && apk update \
    && apk add dumb-init git vim wget curl openssl openssl-dev gcc g++ libffi-dev make zlib-dev libcec-dev libtool openrc python3 python3-dev jq py3-configobj py3-setuptools

## openrc
RUN mkdir -p /run/openrc \
    && touch /run/openrc/softlevel

## python3
RUN mkdir -p ~/.pip \
    && touch ~/.pip/pip.conf \
    && echo "[global]" >> ~/.pip/pip.conf \
    && echo "index-url = http://mirrors.aliyun.com/pypi/simple" >> ~/.pip/pip.conf \
    && echo "[install]" >> ~/.pip/pip.conf \
    && echo "trusted-host=mirrors.aliyun.com" >> ~/.pip/pip.conf
RUN wget https://bootstrap.pypa.io/get-pip.py \
    && python3 get-pip.py

## pip
RUN pip install fastapi uvicorn[standard] openai

EXPOSE 5959

COPY start.sh /start.sh
RUN chmod +x /start.sh
CMD [ "/start.sh" ]
FROM ubuntu:bionic

RUN apt update -y && \
    apt upgrade -y && \
    apt install -y python3-dev python3-pip && \
    pip3 install --no-cache-dir -U pip wheel setuptools

WORKDIR /project

COPY . /project

RUN pip3 install --no-cache-dir -r requirements.txt


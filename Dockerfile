# syntax=docker/dockerfile:1
FROM ubuntu:jammy
WORKDIR /root
RUN mkdir pjproject_docs
COPY . pjproject_docs/
RUN cp /etc/apt/sources.list /etc/apt/sources.list.bak
RUN cat /etc/apt/sources.list.bak | sed "s/archive.ubuntu/sg.archive.ubuntu/" > /etc/apt/sources.list
RUN ln -fs /usr/share/zoneinfo/Asia/Jakarta /etc/localtime
RUN apt-get update -y
RUN DEBIAN_FRONTEND="noninteractive" apt-get install -y tzdata vim tilde git doxygen python3 python3-pip python3-sphinx
RUN cd /root/pjproject_docs && pip3 install -r requirements.txt
EXPOSE 8000
CMD ["/usr/bin/bash", "--init-file", "/root/pjproject_docs/docker/start.sh"]



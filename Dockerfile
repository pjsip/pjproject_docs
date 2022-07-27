# syntax=docker/dockerfile:1
FROM ubuntu:jammy
WORKDIR /root
RUN cp /etc/apt/sources.list /etc/apt/sources.list.bak && \
    cat /etc/apt/sources.list.bak | sed "s/archive.ubuntu/sg.archive.ubuntu/" > /etc/apt/sources.list && \
    ln -fs /usr/share/zoneinfo/Asia/Jakarta /etc/localtime && \
    apt-get update -y && \
    DEBIAN_FRONTEND="noninteractive" apt-get install -y tzdata vim tilde git doxygen python3 python3-pip python3-sphinx
COPY . pjproject_docs/
RUN cd /root/pjproject_docs && \
    pip3 install -r requirements.txt && \
    git restore *
EXPOSE 8000
CMD ["/usr/bin/python3", "-m", "http.server", "--directory=/root/pjproject_docs/docs/build/html/", "8000"]

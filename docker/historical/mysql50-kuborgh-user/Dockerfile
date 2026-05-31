FROM kuborgh/mysql-5.0:latest

ARG uid=1001
ARG gid=1001

RUN addgroup --gid $gid --system mysql \
    && adduser --uid $uid --disabled-password --system --gid $gid mysql \
    && chown -R mysql:mysql /mysql/data

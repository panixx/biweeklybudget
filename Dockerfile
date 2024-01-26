FROM python:3.10-alpine3.16

ARG version
USER root

COPY requirements.txt /tmp/requirements.txt
COPY entrypoint.sh /tmp/entrypoint.sh
COPY biweeklybudget.tar.gz /tmp/biweeklybudget.tar.gz

RUN /usr/local/bin/pip install virtualenv
RUN /usr/local/bin/virtualenv --system-site-packages /app
RUN set -ex \
    && apk add --no-cache \
        fontconfig \
        libxml2 \
        libxml2-dev \
        libxslt \
        libxslt-dev \
        tini \
        git \
        py3-cryptography \
    && apk add --no-cache --virtual .build-deps \
        gcc \
        libffi-dev \
        linux-headers \
        make \
        musl-dev \
        openssl-dev \
    && /app/bin/pip install /tmp/biweeklybudget.tar.gz \
    && /app/bin/pip install gunicorn==19.7.1 \
    && apk del .build-deps \
    && rm -Rf /root/.cache
    && /bin/sed -i " \
                           "\"s/^VERSION =.*/VERSION = '%s+git.%s'/\"" \
                           f" /app/lib/python3.10/site-packages/" \
                           f"biweeklybudget/version.py

RUN install -g root -o root -m 755 /tmp/entrypoint.sh /app/bin/entrypoint.sh

# default to using settings_example.py, and user can override as needed
ENV SETTINGS_MODULE=biweeklybudget.settings_example
ENV LANG=en_US.UTF-8

LABEL com.jasonantman.biweeklybudget.version=$version
LABEL maintainer "jason@jasonantman.com"
LABEL homepage "http://github.com/jantman/biweeklybudget"

EXPOSE 80
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["/app/bin/entrypoint.sh"]

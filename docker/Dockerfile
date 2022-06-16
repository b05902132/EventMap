FROM python:3.9-alpine as dependencies

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"

# git: for cloning https://github.com/jazzband/dj-database-url
# openssl: for https support
RUN apk add --no-cache git openssl

COPY req*.txt ./
RUN pip install --no-cache-dir -r req.txt && \
    pip install --no-cache-dir -r req_git.txt && \
    pip install --no-cache-dir gunicorn



FROM python:3.9-alpine
WORKDIR /opt/EventMap


RUN addgroup -S event_map && adduser -S -H -G event_map event_map && mkdir -p /etc/EventMap && chown event_map /etc/EventMap

# gdal/libspatialite/sqlite: for GeoDjango and SQLite
# openssl: for https support

RUN apk add --no-cache gdal libspatialite sqlite openssl

COPY --from=dependencies /opt/venv /opt/venv
COPY . .

USER event_map

ENV DATABASE_URL="spatialite:////etc/EventMap/db.spatialite"
ENV PATH="/opt/venv/bin:${PATH}"

# Let gunicorn binds to 0:8000 by default
ENV PORT=8000

ENTRYPOINT ["/opt/EventMap/docker/entrypoint.sh"]

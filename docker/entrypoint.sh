#!/bin/sh

# Python can't searches dynamic libraries on POSIX systems without
# gcc or glibc, e.g. Alpine. see https://github.com/python/cpython/pull/18380

search_libraries() {
    ls /lib/"${1}".so* /usr/lib/"${1}".so* /usr/local/lib/"${1}".so* 2>/dev/null
}

PARAM=""

if ! ldconfig -p >/dev/null 2>&1 && ! which gcc ; then
    export GEOS_LIBRARY_PATH="$(search_libraries libgeos_c | head -n1)"
    export GDAL_LIBRARY_PATH="$(search_libraries libgdal | head -n1)"
    export SPATIALITE_LIBRARY_PATH="$(search_libraries mod_spatialite | head -n1)"
fi

PROJECT_ROOT="$(dirname "$0")/../"

cd "${PROJECT_ROOT}"

if [ -f tls.key ] && [ -f tls.crt ] ; then
    if ! [ -r tls.key ]; then
        echo "Can't read from tls.key"
        exit 1
    fi
    if ! [ -r tls.crt ] ; then
        echo "Can't read from tls.crt"
        exit 1
    fi
    PARAM="${PARAM} --keyfile tls.key --certfile tls.crt"
fi

gunicorn CNL_proj.wsgi ${PARAM} "$@"

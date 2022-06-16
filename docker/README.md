A simple docker image for deploying EventMap via gunicorn.

By default this image does not use HTTPS, but Google Maps requries the client to connect via HTTPS, so either
  1. Use a reverse proxy (e.g. Nginx via `docker-compose`) to provide HTTPS connections
  2. Put your ssl certificate, named `tls.crt` and `tls.key`, at the project root, and rebuild the image.
     The startup script will search for those files.


## Configuration

You can config EventMap or gunicorn via environment variables.
The container passes all arguments to gunicorn, so you can also config gunicorn this way.


### Default configuration
By default gunicorn binds to 0:8000.
Database defaults to /etc/EventMap/db.spatialite. You may create a docker volume for that.

# EventMap

A Django app where you can create, view and register events.

Feature:
- Integration with Google Calendar
- Filter events by time and location
- Email notification (TODO)


# Requirements
* [Google Map API Key](https://developers.google.com/maps/documentation/javascript/get-api-key)
* [Google OAuth2](https://developers.google.com/identity/protocols/oauth2) client secret
    * Permission to access Google Calendar.
* [Additional libraries](https://docs.djangoproject.com/en/3.2/ref/contrib/gis/install/#spatial-database) to make sure GeoDjango can access geographic data from database.

Also this app must be served in https. (Required by Google Map)

## Configurable environment variables:

* `DEBUG`: Enables [debug mode](https://docs.djangoproject.com/en/4.0/ref/settings/#debug). Default is false.

### Keys required to access Google services.
* `GOOGLE_MAP_API_KEY`
* `GOOGLE_OAUTH_SECRET`


### Database
* `DATABASE_URL`: The url to your database. Defaults to an in-disk spatialite db if it's empty.
    This app uses [dj-database-url](https://github.com/jazzband/dj-database-url) to make configuration more flexible.
    See [here](https://github.com/jazzband/dj-database-url#url-schema) for the exact URL schema.

* `SECRET_KEY`: [Secret key](https://docs.djangoproject.com/en/4.0/ref/settings/#std-setting-SECRET_KEY) to your database.
    Can't be empty unless `DEBUG` evaluates to true, in which case it use a default key for debugging.

### Library search path
You may want to use environment variable to specify the correct path to the libraries required by GeoDjango:

* `GEOS_LIBRARY_PATH`
* `GDAL_LIBRARY_PATH`
* `SPATIALITE_LIBRARY_PATH`

This is useful on non-glibc systems, e.g. Alpine, because
Python needs glibc to find the correct library path.
(GeoDjango manuals says Python uses `objdump` to find libraries,
but my experiment on Alpine Linux shows that installing `objdump` does not help.)

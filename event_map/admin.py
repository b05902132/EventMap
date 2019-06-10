from django.contrib import admin
from django.contrib.gis.db import models as gisModels
from mapwidgets.widgets import GooglePointFieldWidget
from . import models

# Register your models here.

@admin.register(models.Event, models.LocationConstraint)
class MapAdmin(admin.ModelAdmin):
    formfield_overrides = {
        gisModels.PointField: {'widget': GooglePointFieldWidget},
    }

admin.site.register(models.User)
admin.site.register(models.EventConstraint)
admin.site.register(models.TimeConstraint)


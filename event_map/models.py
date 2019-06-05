from django.contrib.gis.db import models
from django.contrib.gis.geos import Point


class CredentialsField(models.BinaryField): # TODO: should this be hidden?
    description = "Google id credential"

class TimeInterval(models.Model):
    start = models.DateTimeField()
    finish = models.DateTimeField()
    class Meta:
        abstract = True

class Event(TimeInterval):
    name = models.CharField(max_length = 255)
    description = models.TextField()
    coordinate = models.PointField(help_text="Location of this event.")

class User(models.Model):
    email = models.EmailField(primary_key = True)
    credentials = CredentialsField() 

# TODO: default preference
class EventPreference(models.Model): 
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    location = models.PointField() 

    
    

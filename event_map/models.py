import datetime
import rfc3339
import pickle

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.db.models import Q # query object
from .calendar import get_busy_intervals


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
    def get_busy_intervals(self, start, end):
        '''
        Gets time intervals in which the user is busy.
        '''
        return get_busy_intervals(self, start, end)

    def events_to_attend(self, start = None, end = None, *args, **kwargs):
        '''
        Perform a query for all events that the user could attend.
        Start defaults to now, end defaults to one day later.
        '''
        if not start:
            start = datetime.datetime.now()
        if not end:
            end = start + datetime.timedelta(1)

        filter_condition = Q(**kwargs)
        for condition in args:
            filter_condition &= condition
        for interval in self.get_busy_intervals(start, end):
            overlapping = Q(start__range=interval) | Q(finish__range = interval)
            filter_condition &= ~overlapping #exclude overlapping events
        return Event.objects.filter(filter_condition)
            


# TODO: default preference
class EventPreference(models.Model): 
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    location = models.PointField() 

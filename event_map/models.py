import datetime
import rfc3339
import pickle

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.db.models import Q # query object
from django.utils import timezone
from picklefield.fields import PickledObjectField 

from .calendar import get_busy_intervals
from .oauth2 import get_email


class TimeInterval(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    class Meta:
        abstract = True

class Event(TimeInterval):
    name = models.CharField(max_length = 255)
    description = models.TextField(blank = True) # Allow empty description
    location = models.PointField(help_text="Location of this event.")

    @classmethod
    def within_interval(cls, start, end):
        ''' Given a 2-tuple of datetime, query the events within this tuple. '''
        return cls.objects.filter(start__gt=start, end__lt=end)

class User(models.Model):
    google_email = models.EmailField(primary_key = True, editable=False) # Identifier of each user
    credentials = PickledObjectField(editable = False)
    email = models.EmailField()
    notify_before_days = models.IntegerField(default = 1)

    def save(self, *args, **kwargs):
        if not getattr(self, 'google_email', None):
            self.google_email = get_email(self.credentials)
        if not getattr(self, 'email', None):
            self.email = self.google_email
        super().save(*args, **kwargs) 

    def get_busy_intervals(self, start, end):
        '''
        Gets time intervals in which the user is busy.
        '''
        return get_busy_intervals(self.credentials, start, end) 

    def event_filter(self, start, end):
        '''
        Return an object that can be used to query the events the user preferes.
        '''
        filter_condition = Q()
        for constraint in self.eventconstraint_set.all():
            pass #TODO
        for interval in self.get_busy_intervals(start, end):
            overlapping = Q(start__lt=interval.end) & Q(end__gt = interval.start)
            filter_condition &= ~overlapping #exclude overlapping events
        return filter_condition


# TODO: default preference
class EventConstraint(models.Model): 
    user = models.ForeignKey(to=User, on_delete=models.CASCADE) 
    def get_filter(self):
        pass #TODO
    @staticmethod
    def default_preference(user):
        pass #TODO

class TimeConstraint(models.Model):
    link = models.OneToOneField(primary_key = True, to = EventConstraint, on_delete = models.CASCADE)
    def get_filter(self):
        pass # TODO

class LocationConstraint(models.Model):
    link = models.OneToOneField(primary_key = True, to = EventConstraint, on_delete = models.CASCADE)
    location = models.PointField()
    distance = models.FloatField() # In kilometer
    def get_filter(self):
        return Q(distance__lte = (self.location, Distance(km=self.distance)))


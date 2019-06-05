import datetime
import pickle
import os.path
from itertools import chain
from collections import namedtuple

from rfc3339 import parse_datetime, datetimetostr
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

TimeInterval = namedtuple('TimeInterval',('start', 'end'))

def to_time_interval(start_s, end_s):
    """
    Convert a pair of rfc3339 strings to TimeInterval.
    """
    return TimeInterval(parse_datetime(start_s), parse_datetime(end_s))

def get_busy_intervals(user, start=None, end=None, *, calendars = ['primary']):
    '''
    Gets time intervals in which the user is busy.
    start defaults to now, end defaults to one day later.

    Calendars are for future expansion, when the users may have more than 1 calendars.
    '''
    if not start:
        start = datetime.datetime.utcnow()
    if not end:
        end = start + datetime.timedelta(1)
    credentials = pickle.loads(user.credentials)
    calendar = build('calendar', 'v3', credentials=credentials) 
    request = { "items":[{ "id" : name} for name in calendars] ,"timeMin":datetimetostr(start), "timeMax":datetimetostr(end)}
    response = calendar.freebusy().query(body=request).execute()
    busy_lists = [response['calendars'][calendar_name]['busy'] for calendar_name in calendars]
    busy_intervals = chain(*busy_lists) 
    return [ to_time_interval(*interval.values()) for interval in busy_intervals ]

def test():
    from .models import User
    me = User.objects.all()[0]
    me.get_busy_intervals(datetime.datetime.now(), datetime.datetime.now()+datetime.timedelta(30))

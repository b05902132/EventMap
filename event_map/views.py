from functools import wraps
from datetime import datetime, timedelta, timezone
import google.oauth2.credentials

from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, DetailView, ListView, UpdateView
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.utils.timezone import get_current_timezone

from .oauth2 import get_flow, get_email 
from . import models, forms
from .models import User, Event

# TODO imporve on detail view
class EventEditView(UpdateView):
    form_class = forms.EventForm
    model = Event
    template_name = "event_map/event_edit.html"


class EventCreateView(FormView):
    template_name = "event_map/event_create.html"
    form_class = forms.EventForm
    success_url = reverse_lazy("event_map:event_map")

def require_login(view):
    ''' Ensure only registered user can access the view. '''
    @wraps(view)
    def new_view(request, *args, **kwargs):
        pk = request.session.get('user', None)
        if not pk:
            return HttpResponseRedirect(reverse('event_map:login'))
        query = User.objects.filter(pk=pk)
        if not query:
            return HttpResponseRedirect(reverse('event_map:login'))
        return view(request, *args, **kwargs)
    return new_view

def parse_datetime(dict_obj, name, default = None):
    string = dict_obj.get(name, None)
    if string:
        ret = datetime.strptime(string, '%Y-%m-%dT%H:%M')
        ret = ret.replace(tzinfo=get_current_timezone()) 
        return ret 
    else:
        return default

def event_map(request):
    user = get_user(request)
    is_logged_in = bool(user)

    start = parse_datetime(request.GET, 'start', datetime.now(timezone.utc))
    end = parse_datetime(request.GET, 'end', start + timedelta(30))
    events = Event.within_interval(start, end)
    if user:
        events = events.filter(user.event_filter(start, end))
    return render(request, 'event_map/index.html', {'event_list': events, 'is_logged_in':is_logged_in, 'form': forms.FilterForm()})

### The following functions are for user management.  

def get_user(request):
    try:
        return User.objects.filter(pk=request.session['user']).get()
    except (KeyError, models.User.DoesNotExist):
        return None 

def login(request):
    ''' asks for google account login '''
    flow = get_flow()
    flow.redirect_uri = request.build_absolute_uri(reverse('event_map:oauth2_callback'))
    authorization_uri, state = flow.authorization_url(
            access_type='offline',
            include_granted_scope='true')
    request.session['state'] = state
    return HttpResponseRedirect(authorization_uri)

def logout(request):
    request.session.pop('user', None)
    return HttpResponseRedirect(reverse('event_map:event_map'))

def oauth2_callback(request):
    ''' Google redirects user back to here, where we add the user's google account data into the database. '''
    state = request.session.get('state', None)
    if not state:
        return HttpResponseRedirect(reverse('event_map:login'))

    flow = get_flow(state=state)
    flow.redirect_uri = request.build_absolute_uri(reverse('event_map:oauth2_callback'))
    authorization_response = request.get_raw_uri()
    flow.fetch_token(authorization_response = authorization_response)
    credentials = flow.credentials
    pk = get_email(credentials)
    try:
        user = User.objects.filter(pk=pk).get()
        # Update credential
        user.credentials = credentials
        user.save()
    except User.DoesNotExist:
        user = User.objects.create(credentials=credentials)
    request.session['user'] = user.pk
    return HttpResponseRedirect(reverse('event_map:event_map'))

import pickle

from django.urls import reverse
from django.views.generic import FormView, DetailView
from django.http import HttpResponse, HttpResponseRedirect
import google.oauth2.credentials
from .oauth2 import get_flow, get_email

from . import models
from .models import User


def event_map(request):
    user = get_user(request)
    if not user:
        return HttpResponseRedirect(reverse('event_map:oauth2_authorize'))
    # TODO: show event_map
    # TODO: show filter
    return HttpResponse('Under construction!')

### The following functions are for user registeration.
def get_user(request):
    pk = request.session.get('user', None)
    if not pk:
        return None
    query = User.objects.filter(pk=pk)
    if not query:
        return None
    return query.get()
    

def register(request):
    state = request.session.get('state', None)
    if not state:
        return HttpResponseRedirect(reverse('event_map:oauth2_authorize'))

    flow = get_flow(state=state)
    flow.redirect_uri = request.build_absolute_uri(reverse('event_map:register'))
    authorization_response = request.get_raw_uri()
    breakpoint()
    flow.fetch_token(authorization_response = authorization_response)
    credentials = flow.credentials
    email = get_email(credentials)
    try:
        user = User.objects.filter(email=email).get()
    except User.DoesNotExist:
        user = User.objects.create(email=email, credentials=pickle.dumps(credentials))
    request.session['user'] = user.pk
    return HttpResponseRedirect(reverse('event_map:event_map'))

def oauth2_authorize(request):
    flow = get_flow()
    flow.redirect_uri = request.build_absolute_uri(reverse('event_map:register'))
    authorization_uri, state = flow.authorization_url(
            access_type='offline',
            include_granted_scope='true')
    request.session['state'] = state
    return HttpResponseRedirect(authorization_uri)


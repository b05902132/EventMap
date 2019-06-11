from django.urls import path
from django.conf.urls import url, include

from . import views

app_name = 'event_map'
urlpatterns = [
    path('oauth2_callback', views.oauth2_callback, name='oauth2_callback'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('', views.event_map, name='event_map'),
    path('event/create', views.EventCreateView.as_view(), name="create"),
]

url(r'^select2/', include('django_select2.urls')),

from django.urls import path

from . import views

app_name = 'event_map'
urlpatterns = [
    path('register', views.register, name='register'),
    path('oauth2_authorize', views.oauth2_authorize, name='oauth2_authorize'),
    path('', views.event_map, name='event_map'),
]

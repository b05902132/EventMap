from django import forms
from django.contrib.admin import widgets

# TODO: make forms for register event


from event_map.models import Event
from mapwidgets.widgets import GooglePointFieldWidget, GoogleStaticMapWidget, GoogleStaticOverlayMapWidget


class EventCreateForm(forms.ModelForm): 
    class Meta:
        model = Event
        fields = ("name", "description", "start", "end", "location")
        widgets = {
            'location': GooglePointFieldWidget,
        }


class EventDetailForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ("name", "description", "location")
        widgets = {
            'location': GoogleStaticMapWidget(zoom=12, size="240x240"),
        } 

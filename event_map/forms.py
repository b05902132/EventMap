from django import forms
from django.contrib.admin import widgets

from event_map.models import Event
from mapwidgets.widgets import GooglePointFieldWidget, GoogleStaticMapWidget, GoogleStaticOverlayMapWidget

class DateTimeInputHTML5(forms.DateTimeInput):
    input_type = 'datetime-local'

class DateTimeFieldHTML5(forms.DateTimeField):
    def __init__(self, *args, **kwargs):
        kwargs['input_formats'] = ['%Y-%m-%dT%H:%M']
        kwargs['widget'] = DateTimeInputHTML5()
        super().__init__(*args, **kwargs)


class EventForm(forms.ModelForm): 
    start = DateTimeFieldHTML5()
    end = DateTimeFieldHTML5()
    class Meta:
        model = Event
        fields = ("name", "description", "start", "end", "location")
        widgets = {
            'location': GooglePointFieldWidget,
        }

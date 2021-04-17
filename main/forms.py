import django.forms as forms
from mapbox_location_field.forms import LocationField


class LocationPickerForm(forms.Form):
    location = LocationField()
    radius = forms.NumberInput
    time = forms.TimeField

#pog
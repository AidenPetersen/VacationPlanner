from django import forms
from .models import LocationPickerModel
from mapbox_location_field import forms as f


class LocationPickerForm(forms.ModelForm):
    class Meta:
        model = LocationPickerModel
        fields = "__all__"

from django import forms
from .models import LocationPickerModel


class LocationPickerForm(forms.ModelForm):
    class Meta:
        model = LocationPickerModel
        fields = "__all__"

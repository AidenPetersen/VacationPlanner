from django import forms
import floppyforms as ff


class LocationPickerForm(forms.Form):
    location = ff.gis.PointField()
    radius = forms.NumberInput()
    time = forms.TimeField()

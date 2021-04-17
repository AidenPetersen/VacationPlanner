from django.db import models
from mapbox_location_field.models import LocationField


class LocationPickerModel(models.Model):
    location = LocationField(map_attrs={"style": "mapbox://styles/mightysharky/cjwgnjzr004bu1dnpw8kzxa72", "center": [-91.5550, 41.6627], "marker_color": 'blue'})
    radius = models.IntegerField()
    time = models.TimeField()
from django.shortcuts import render
from .forms import LocationPickerForm

# Create your views here.
from django.shortcuts import render


def home(request):
    location_form = LocationPickerForm()

    return render(request, 'base.html', {
        'form': location_form
    })

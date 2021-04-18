from django.shortcuts import render, redirect
from .forms import LocationPickerForm
from .utility import *


def home(request):
    location_form = LocationPickerForm()

    if request.method == 'POST':
        f = LocationPickerForm(request.POST)

        if f.is_valid():
            print(f.data)
            request.session['data'] = f.data
            return redirect(analysis)

    return render(request, 'form.html', {
        'form': location_form
    })


def analysis(request):
    data = request.session['data']
    location = data['location'].split(',')
    lat = location[0]
    long = location[1]
    attractions = format_attractions(lat, long, int(data['radius']) * 1609)
    attractions_names = [x[0] for x in attractions]
    attractions_ratings = [x[1] for x in attractions]
    attractions_types = [x[2]['kinds'] for x in attractions]
    frontend = prep_frontend(attractions_names, attractions_ratings, attractions_types)
    return render(request, 'analysis.html', {
        'attractions_tuples': attractions,
        'location': data['location'],
        'days': data['days'],
        'radius': data['radius'],
        'frontend': frontend
    })


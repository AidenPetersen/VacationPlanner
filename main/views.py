from django.shortcuts import render, redirect
from .forms import LocationPickerForm
from .utility import *


def home(request):
    location_form = LocationPickerForm()

    if request.method == 'POST':
        f = LocationPickerForm(request.POST)

        if f.is_valid():
            # print(f.data)
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
    print(f"days = {data['days']}")
    print(f"radius = {data['radius']}")
    attractions, food = format_attractions(lat, long, int(data['radius']) * 1609)
    path = get_path(lat, long, int(data['days']), int(data['radius']), attractions, food)
    print(path)
    return render(request, 'analysis.html', {
        'path': path
    })

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
    l = data['location'].split(',')
    lat = l[0]
    long = l[1]
    attractions_list = otm_get("radius", radius_query(lat, long, int(data['radius']) * 1609))
    print(attractions_list)

    attractions_names = [x['name'] for x in attractions_list]
    return render(request, 'analysis.html', {
        'attractions_names': attractions_names,
        'location': data['location'],
        'days': data['days'],
        'radius': data['radius']
    })

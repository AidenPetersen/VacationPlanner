from django.shortcuts import render, redirect
from .forms import LocationPickerForm
import requests

# Create your views here.
from django.shortcuts import render


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
    return render(request, 'analysis.html', {
        'location': data['location'],
        'days': data['days'],
        'radius': data['radius']
    })


def radiusquery(lat, long, rad):
    str = f"radius={rad}&limit=25&offset=0&lat={lat}&lon={long}&format=json"
    return str

def otmget(method, query):
    OTM_KEY = "5ae2e3f221c38a28845f05b6e93dcff7317a493d8bb313a3fd186d0c"

    reqstr = "https://api.opentripmap.com/0.1/en/places/"
    reqstr += method + "?apikey="+ OTM_KEY + "&" + query
    r = requests.get(reqstr)
    print(r.text)

#otmget("radius",radiusquery(41.66127,-91.53680, 1000))




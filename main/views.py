from django.shortcuts import render, redirect
from .forms import LocationPickerForm

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
        'data': data,
    })

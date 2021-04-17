from django.shortcuts import render, redirect
from .forms import LocationPickerForm

# Create your views here.
from django.shortcuts import render


def home(request):
    location_form = LocationPickerForm()

    # if request.method == 'POST':
    #     f = LocationPickerForm(request.POST)
    #     if location_form.is_valid():
    #         return redirect(request, )



    return render(request, 'form.html', {
        'form': location_form
    })

# def analysis(request, data):
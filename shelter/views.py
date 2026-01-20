from django.shortcuts import render
from .models import Animal
from django import http

# Create your views here.
def animal_list(request): # Shows all animals. I followed the book pretty close on the project becuase I didn't feel comfortable going to far out
    animals = Animal.object.all()
    return render(
        request,
        'shelter/animals/list.html',
        {'animals': animals }
    )

def animal_view(request, id):
    try:
        animal_profile = Animal.get(id=id)
    except:
        raise http.Http404("No animal found")
    return render(
        request,
        'shelter/detail.html',
        {'animal_profile': animal_profile}
    )

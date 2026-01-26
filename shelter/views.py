from django.shortcuts import render
from .models import Animal
from django import http
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailAnimalForm
from django.core.mail import send_mail



# Create your views here.
def animal_list(request): # Shows all animals. I followed the book pretty close on the project becuase I didn't feel comfortable going to far out
    animal_list = Animal.adoptable.all()
    paginator = Paginator(animal_list, 2)
    page_number = request.GET.get('page',1)
    try:
        animals = paginator.page(page_number)
    except EmptyPage:
        animals = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        animals = paginator.page(1)
    return render(
        request,
        'shelter/animals/list.html',
        {'animals': animals}
    )

def animal_view(request, species,breed,name):
    animal_profile = get_object_or_404(Animal, species = species, breed=breed,name = name)
    return render(
        request,
        'shelter/animals/detail.html',
        {'animal_profile': animal_profile}
    )

class AnimalListView(ListView):
    queryset = Animal.adoptable.all()
    context_object_name = 'animals'
    paginate_by = 2
    template_name = 'shelter/animals/list.html'

def animal_share(request, animal_id):
    animal = get_object_or_404(Animal, id = animal_id)
    sent = False
    if request.method =="POST":
        form = EmailAnimalForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            animal_url = request.build_absolute_uri(animal.get_absoulute_url())
            subject = (
                f"{cd['name']} ({cd['email']})"
                f"Wants you to meet {animal.name}"
                )
            message = (
                f"{animal.name} is a {animal.breed}. They are {animal.desc}, and can't wait to come home with you tonight!"
                )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd['to']]
                )
            sent = True
    else:
        form = EmailAnimalForm()
    return render(request,'shelter/animals/share.html',{
            'animal': animal,
            'form': form,
            'sent': sent
            })

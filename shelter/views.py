from django.shortcuts import render
from .models import Animal, Volunteer
from django import http
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailAnimalForm, SearchForm, LoginForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.contrib.postgres.search import SearchVector
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import JsonResponse, HttpResponseRedirect
from .favorite import Favorite
from django.urls import reverse



# Create your views here.
def animal_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = (Animal.adoptable.annotate(search=SearchVector('species', 'breed'),).filter(search=query))
    return render(request, 'shelter/animals/search.html',{
        'form':form,
        'query':query,
        'results':results
    })


def animal_list(request, tag_slug =None): # Shows all animals.
    animal_list = Animal.adoptable.all()
    favorites = Favorite(request)
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug = tag_slug)
        animal_list = animal_list.filter(tags__in=[tag])
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
        {'animals': animals,
         'tag': tag,
         'favorites': favorites,
        }
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

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password'],
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Successful!")
                else:
                    return HttpResponse("Unsuccesseful")
            else:
                return HttpResponse("Invalid login")
    else:
        form = LoginForm()
    return render(request, 'shelter/login.html', {'form':form})

def volunteer_list(request):
    # prefetch_related fetches all related animals in 1 extra query instead of N
    volunteers = Volunteer.objects.prefetch_related(
        'volunteeranimalcare_set__animal'  # traverses through the intermediary table
    ).all()
    return render(request, 'shelter/volunteer_list.html', {'volunteers': volunteers})


def animal_stats(request):
    # Try to get from Redis cache first
    animal_count = cache.get('animal_count')

    if animal_count is None:
        # Cache miss — query the DB and store in Redis for 60 seconds
        animal_count = Animal.objects.count()
        cache.set('animal_count', animal_count, timeout=60)
        source = "database"
    else:
        source = "Redis cache"

    return render(request, 'shelter/stats.html', {
        'animal_count': animal_count,
        'source': source,
    })

def get_favorite(request):
     favorites = Favorite(request)
     return JsonResponse({'favorites': favorites.get_ids(), 'count': len(favorites)})

def toggle_favorite(request, animal_id):
    animal = get_object_or_404(Animal, pk=animal_id)
    favorites = Favorite(request)
    favorites.toggle(animal)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'count': len(favorites), 'is_favorited': animal in favorites})
    return HttpResponseRedirect(reverse('animal_list'))

def favorites_page(request):
    favorite_ids = request.session.get('favorite_animals', [])
    favorite_animals = Animal.objects.filter(pk__in=favorite_ids)
    return render(request, 'favorites.html', {'animals': favorite_animals})


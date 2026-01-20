from django.urls import path
from . import views
app_name = 'animal_shelter'
urlpatterns = [
    path('', views.animal_list, name='animal_list'), # defaults to my list of animals
    path('<int:id>/', views.animal_view, name='animal_view'),
]
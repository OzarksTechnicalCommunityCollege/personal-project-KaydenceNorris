from django.urls import path
from . import views
app_name = 'animal_shelter'
urlpatterns = [
    # path('', views.animal_list, name='animal_list'), # defaults to my list of animals
    path('', views.AnimalListView.as_view(), name='animal_list'),
    path('<str:species>/<str:breed>/<str:name>', views.animal_view, name='animal_view'),
    path('<int:animal_id>/share/', views.animal_share, name='animal_share')
]
from django.urls import path
from . import views
app_name = 'animal_shelter'
urlpatterns = [
    path('', views.animal_list, name='animal_list'), # defaults to my list of animals
    # path('', views.AnimalListView.as_view(), name='animal_list'),
    path('<str:species>/<str:breed>/<str:name>', views.animal_view, name='animal_view'),
    path('<int:animal_id>/share/', views.animal_share, name='animal_share'),
    path('tag/<slug:tag_slug>/', views.animal_list, name="animals_by_tag"),
    path('search/', views.animal_search, name='animal_search'),
    path('login/', views.user_login, name='login'),
    path('animals/favorites/', views.favorites_page, name='favorites'),
    path('animals/<int:animal_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
]
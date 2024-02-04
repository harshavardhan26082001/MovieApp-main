from django.contrib import admin
from django.urls import path, include
from django.views.decorators.cache import cache_page
from . import views

urlpatterns = [
    path('', views.Movies, name='Movies'),
    path('login',views.login,name='login'),
    path('register', views.register, name='register'),
    path('logout',views.logout,name='logout'),
    path('movie_details/<movie_id>', views.movie_details, name='movie_details'),
    path('series_details/<series_id>', views.series_details, name='series_details'),
    path('add_movie/', views.add_movie, name='add_movie'),
    path('search_details/', views.search_details, name='search_details'),
    path('search_details/login', views.login, name='login'),
    path('search_details/register', views.register, name='register'),
]
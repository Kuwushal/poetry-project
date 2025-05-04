from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_poem, name='search_poem'),
    path('poem/<str:title>/', views.poem_detail, name='poem_detail'),
    path('write/', views.write_poem, name='write_poem'),
]

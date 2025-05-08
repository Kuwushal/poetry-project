from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_poem, name='search_poem'),
    path('poem/<str:title>/', views.poem_detail, name='poem_detail'),
    path('write/', views.write_poem, name='write_poem'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_views, name='signup'),
    path('profile/', views.profile_view, name='profile'), 
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
]



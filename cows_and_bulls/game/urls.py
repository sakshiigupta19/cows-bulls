from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('check_guess/', views.check_guess, name='check_guess'),
    path('new_game/', views.new_game, name='new_game'),
]

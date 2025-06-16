from django.shortcuts import redirect
from django.urls import path
from . import views

urlpatterns = [
    path('', lambda request: redirect('chantiers/')), 
    path('ajouter/', views.ajouter_chantier, name='ajouter_chantier'),
    path('get-chantier-details/', views.get_chantier_details, name='get_chantier_details'),


  
]



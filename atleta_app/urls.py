from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastrarAtleta/', views.cadastrarAtleta, name='cadastrarAtleta'),
    path('visualizarAtleta/', views.visualizarAtleta, name='visualizarAtleta'),
]

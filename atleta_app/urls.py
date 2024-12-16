from django.urls import path
from . import views


# URLs do sistema

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastrarAtleta/', views.cadastrarAtleta, name='cadastrarAtleta'),
    path('visualizarAtleta/', views.visualizarAtleta, name='visualizarAtleta'),
]

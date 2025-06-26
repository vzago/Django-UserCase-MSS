from django.urls import path
from . import views


# URLs do sistema

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('cadastrarAtleta/', views.cadastrar_atleta, name='cadastrarAtleta'),
    path('visualizarAtleta/', views.visualizar_atleta, name='visualizarAtleta'),
    path('estatisticas/', views.estatisticas_atletas, name='estatisticas'),
]

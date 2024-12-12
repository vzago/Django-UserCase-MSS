from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Atleta
from .forms import AtletaForm

# Home
def home(request):
    return render(request, 'atleta_app/home.html')

# Cadastrar Atleta
def cadastrarAtleta(request):
    if request.method == 'POST':
        form = AtletaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Atleta cadastrado com sucesso!')
            return redirect('home')  # Redireciona para a página inicial
    else:
        form = AtletaForm()
    return render(request, 'atleta_app/cadastrarAtleta.html', {'form': form})

# Visualizar Atleta
def visualizarAtleta(request):
    cpf = request.GET.get('cpf')
    atleta = None
    error_message = None

    if cpf:
        try:
            atleta = Atleta.objects.get(cpf=cpf)
        except Atleta.DoesNotExist:
            error_message = 'Atleta não encontrado. Verifique o CPF digitado.'

    return render(request, 'atleta_app/visualizarAtleta.html', {'atleta': atleta, 'error_message': error_message})
    
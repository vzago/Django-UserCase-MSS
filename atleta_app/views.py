from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Atleta
from .forms import AtletaForm

# Home
def home(request):
    return render(request, 'atleta_app/home.html')

# Cadastrar Atleta
def cadastrarAtleta(request):
    
    # Verifica se o formulário foi submetido
    if request.method == 'POST':
        form = AtletaForm(request.POST)
        # Verifica se o formulário é válido
        if form.is_valid():
            form.save()
            messages.success(request, 'Atleta cadastrado com sucesso!')
            return redirect('home')  # Redireciona para a página inicial
        
    # Se o formulário não foi submetido, cria um formulário em branco
    else:
        form = AtletaForm()
    return render(request, 'atleta_app/cadastrarAtleta.html', {'form': form})

# Visualizar Atleta
def visualizarAtleta(request):
    cpf = request.GET.get('cpf')
    atleta = None
    error_message = None

    # Verifica se foi informado um CPF
    if cpf:
        try:
            atleta = Atleta.objects.get(cpf=cpf)
        except Atleta.DoesNotExist:
            error_message = 'Atleta não encontrado. Verifique o CPF digitado.'
            
    # Se não foi informado um CPF, exibe a mensagem de erro
    return render(request, 'atleta_app/visualizarAtleta.html', {'atleta': atleta, 'error_message': error_message})
    
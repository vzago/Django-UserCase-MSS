from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseNotAllowed
from .models import Atleta
from .forms import AtletaForm, UserRegistrationForm, UserLoginForm

# Home
def home(request):
    return render(request, 'atleta_app/home.html')

# Login - Allow GET and POST only
@require_http_methods(["GET", "POST"])
@csrf_protect
def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo, {user.first_name}!')
                return redirect('home')
            else:
                messages.error(request, 'Usuário ou senha incorretos.')
    else:
        form = UserLoginForm()
    
    return render(request, 'atleta_app/login.html', {'form': form})

# Logout - Allow POST only for security
@require_http_methods(["POST"])
@csrf_protect
def user_logout(request):
    logout(request)
    messages.success(request, 'Você foi desconectado com sucesso.')
    return redirect('home')

# Register - Allow GET and POST only
@require_http_methods(["GET", "POST"])
@csrf_protect
def user_register(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Conta criada com sucesso!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'atleta_app/register.html', {'form': form})

# Cadastrar Atleta
@login_required
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
@login_required
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
    
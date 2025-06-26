from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseNotAllowed
from django.core.cache import cache
from .models import Atleta
from .forms import AtletaForm, UserRegistrationForm, UserLoginForm
import json

# Home
def home(request):
    # Cache da página home por 10 minutos
    cache_key = 'home_page'
    cached_content = cache.get(cache_key)
    
    if cached_content is None:
        # Busca estatísticas otimizadas
        estatisticas = Atleta.get_atletas_estatisticas()
        cached_content = {'estatisticas': estatisticas}
        cache.set(cache_key, cached_content, 600)  # 10 minutos
    
    return render(request, 'atleta_app/home.html', cached_content)

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
def cadastrar_atleta(request):
    
    # Verifica se o formulário foi submetido
    if request.method == 'POST':
        form = AtletaForm(request.POST)
        # Verifica se o formulário é válido
        if form.is_valid():
            form.save()
            # Limpa cache relacionado após cadastro
            # Deleta chaves específicas em vez de usar delete_pattern
            cache.delete('home_page')
            cache.delete('atletas_estatisticas')
            # Limpa cache de busca de atletas (chaves específicas)
            cache.delete('atleta_search_all')
            cache.delete('atleta_search_cpf')
            cache.delete('atleta_search_nome')
            cache.delete('atleta_search_clube')
            cache.delete('atleta_search_posicao')
            messages.success(request, 'Atleta cadastrado com sucesso!')
            return redirect('home')  # Redireciona para a página inicial
        
    # Se o formulário não foi submetido, cria um formulário em branco
    else:
        form = AtletaForm()
    return render(request, 'atleta_app/cadastrarAtleta.html', {'form': form})

# Visualizar Atleta
@login_required
def visualizar_atleta(request):
    cpf = request.GET.get('cpf', '').strip()
    nome = request.GET.get('nome', '').strip()
    clube = request.GET.get('clube', '').strip()
    posicao = request.GET.get('posicao', '').strip()

    # Usa o método centralizado do modelo com cache habilitado
    atletas, error_message = Atleta.visualizar_atleta(
        cpf=cpf if cpf else None,
        nome=nome if nome else None,
        clube=clube if clube else None,
        posicao=posicao if posicao else None,
        use_cache=True
    )

    return render(request, 'atleta_app/visualizarAtleta.html', {
        'atletas': atletas,
        'cpf': cpf,
        'nome': nome,
        'clube': clube,
        'posicao': posicao,
        'error_message': error_message
    })

# Estatísticas dos Atletas
@login_required
def estatisticas_atletas(request):
    """
    View otimizada para mostrar estatísticas dos atletas.
    Usa cache e consultas otimizadas do banco de dados.
    """
    # Cache das estatísticas por 15 minutos
    cache_key = 'atletas_estatisticas'
    estatisticas = cache.get(cache_key)
    atletas_qs = Atleta.objects.all().only('nome', 'idade', 'altura', 'peso', 'numeroTotalDeJogos', 'numeroDeJogosComoTitular')
    atletas_list = list(atletas_qs.values('nome', 'idade', 'altura', 'peso', 'numeroTotalDeJogos', 'numeroDeJogosComoTitular'))

    # Dados para gráfico de faixa etária
    faixa_1 = sum(18 <= a['idade'] <= 22 for a in atletas_list)
    faixa_2 = sum(23 <= a['idade'] <= 27 for a in atletas_list)
    faixa_3 = sum(28 <= a['idade'] <= 32 for a in atletas_list)
    faixa_4 = sum(a['idade'] >= 33 for a in atletas_list)
    faixas_etarias = [faixa_1, faixa_2, faixa_3, faixa_4]

    # Dados para gráfico de jogos por atleta
    nomes_atletas = [a['nome'] for a in atletas_list]
    total_jogos = [a['numeroTotalDeJogos'] for a in atletas_list]
    jogos_titular = [a['numeroDeJogosComoTitular'] for a in atletas_list]

    if estatisticas is None:
        estatisticas = Atleta.get_atletas_estatisticas()
        cache.set(cache_key, estatisticas, 900)  # 15 minutos
    
    return render(request, 'atleta_app/estatisticas.html', {
        'estatisticas': estatisticas,
        'faixas_etarias_json': json.dumps(faixas_etarias),
        'nomes_atletas_json': json.dumps(nomes_atletas),
        'total_jogos_json': json.dumps(total_jogos),
        'jogos_titular_json': json.dumps(jogos_titular),
        'estatisticas_json': json.dumps(estatisticas),
        'atletas_list': atletas_list,
    })
    
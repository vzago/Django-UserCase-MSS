from django.db import models
import re
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.core.cache import cache

# Create your models here.
class Atleta(models.Model):
    
    #Atributos do Atleta que serão armazenados no banco de dados
    nome = models.CharField(max_length=100, db_index=True)  # Índice para busca por nome
    cpf = models.CharField(unique = True, max_length=14, db_index=True)  # Índice para busca por CPF
    idade = models.IntegerField()
    altura = models.FloatField()
    clube = models.CharField(max_length=100, db_index=True)  # Índice para busca por clube
    peso = models.FloatField()
    posicao = models.CharField(max_length=100, db_index=True)  # Índice para busca por posição
    numeroTotalDeJogos = models.IntegerField()
    numeroDeJogosComoTitular = models.IntegerField()
    
    class Meta:
        indexes = [
            models.Index(fields=['nome']),
            models.Index(fields=['cpf']),
            models.Index(fields=['clube']),
            models.Index(fields=['posicao']),
            models.Index(fields=['nome', 'clube']),  # Índice composto para buscas múltiplas
            models.Index(fields=['clube', 'posicao']),  # Índice composto para buscas múltiplas
        ]
    
    #Método para registrar um atleta no banco de dados.
    
    def registrar_atleta(self):
        self.save()
        
    
    @classmethod
    def visualizar_atleta(cls, cpf=None, nome=None, clube=None, posicao=None, use_cache=True):
        """
        Método centralizado para visualizar atletas com diferentes filtros.
        Prioridade: CPF (busca exata) > outros filtros (busca parcial)
        Inclui otimizações de performance com cache e índices.
        """
        # Gera chave de cache baseada nos parâmetros
        cache_key = f"atleta_search_{cpf}_{nome}_{clube}_{posicao}"
        
        # Tenta buscar do cache se habilitado
        if use_cache:
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result
        
        # Filtro por CPF (busca exata, prioridade)
        if cpf:
            try:
                # Otimização: usa only() para buscar apenas campos necessários
                atleta = cls.objects.only(
                    'nome', 'cpf', 'idade', 'altura', 'clube', 'peso', 
                    'posicao', 'numeroTotalDeJogos', 'numeroDeJogosComoTitular'
                ).get(cpf=cpf)
                result = ([atleta], None)
            except ObjectDoesNotExist:
                result = ([], 'Atleta não encontrado. Verifique o CPF digitado.')
        else:
            # Filtros parciais com otimizações
            # Usa Q objects para queries mais eficientes
            filters = Q()
            
            if nome:
                filters &= Q(nome__icontains=nome)
            if clube:
                filters &= Q(clube__icontains=clube)
            if posicao:
                filters &= Q(posicao__icontains=posicao)
            
            # Otimização: usa only() para buscar apenas campos necessários
            # e order_by() para garantir ordem consistente
            atletas = cls.objects.only(
                'nome', 'cpf', 'idade', 'altura', 'clube', 'peso', 
                'posicao', 'numeroTotalDeJogos', 'numeroDeJogosComoTitular'
            ).filter(filters).order_by('nome')
            
            result = (atletas, None)
        
        # Salva no cache por 5 minutos se habilitado
        if use_cache:
            cache.set(cache_key, result, 300)  # 5 minutos
        
        return result
    
    @classmethod
    def get_atletas_estatisticas(cls):
        """
        Método otimizado para buscar estatísticas dos atletas.
        Usa annotate() para cálculos no banco de dados.
        """
        from django.db.models import Avg, Count, Max, Min
        
        return cls.objects.aggregate(
            total_atletas=Count('id'),
            media_idade=Avg('idade'),
            media_altura=Avg('altura'),
            media_peso=Avg('peso'),
            max_jogos=Max('numeroTotalDeJogos'),
            min_jogos=Min('numeroTotalDeJogos')
        )
        
    def __str__(self):
        return self.nome
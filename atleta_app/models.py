from django.db import models
import re
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.
class Atleta(models.Model):
    
    #Atributos do Atleta que serão armazenados no banco de dados
    nome = models.CharField(max_length=100)
    cpf = models.CharField(unique = True, max_length=14)
    idade = models.IntegerField()
    altura = models.FloatField()
    clube = models.CharField(max_length=100)
    peso = models.FloatField()
    posicao = models.CharField(max_length=100)
    numeroTotalDeJogos = models.IntegerField()
    numeroDeJogosComoTitular = models.IntegerField()
    
    #Método para registrar um atleta no banco de dados.
    
    def registrarAtleta(self):
        self.save()
        
    
    def visualizarAtleta(cpf):
        #Verificar se o Atleta está cadastrado no banco de dados
        try:
            atleta = Atleta.objects.get(cpf = cpf)
            #se estiver retorna o atleta
            return atleta
        
        #Se não estiver retorna False
        except ObjectDoesNotExist:
            
            return False 
        
    def __str__(self):
        return self.nome
from django import forms
from .models import Atleta
import re


# Formulário para cadastro de atletas
class AtletaForm(forms.ModelForm):
    class Meta:
        model = Atleta
        # Campos que serão exibidos no formulário
        fields = [
            'nome',
            'cpf',
            'idade',
            'altura',
            'clube',
            'peso',
            'posicao',
            'numeroTotalDeJogos',
            'numeroDeJogosComoTitular',
        ]
    
    # Validação personalizada para o CPF -  Formato xxx.xxx.xxx-xx
    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        formato = re.compile(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$')
        if not formato.match(cpf):
            raise forms.ValidationError("O CPF deve estar no formato xxx.xxx.xxx-xx")
        return cpf
    
    # Validação para garantir que número de jogos como titular <= número total de jogos
    def clean_numeroDeJogosComoTitular(self):
        total_jogos = self.cleaned_data.get('numeroTotalDeJogos')
        jogos_titular = self.cleaned_data.get('numeroDeJogosComoTitular')
        if jogos_titular > total_jogos:
            raise forms.ValidationError("O número de jogos como titular não pode exceder o número total de jogos.")
        return jogos_titular

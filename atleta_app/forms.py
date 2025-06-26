from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Atleta
import re


# Formulário para cadastro de atletas
class AtletaForm(forms.ModelForm):
    class Meta:
        model = Atleta
        fields = ['nome', 'cpf', 'idade', 'altura', 'clube', 'peso', 'posicao', 'numeroTotalDeJogos', 'numeroDeJogosComoTitular']
        widgets = {
            'altura': forms.NumberInput(attrs={'step': '0.01'}),
            'peso': forms.NumberInput(attrs={'step': '0.1'}),
        }
    
    # Validação personalizada para o CPF -  Formato xxx.xxx.xxx-xx
    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        # Remove caracteres não numéricos
        cpf = re.sub(r'[^0-9]', '', cpf)
        
        # Verifica se tem 11 dígitos
        if len(cpf) != 11:
            raise forms.ValidationError("CPF deve ter 11 dígitos.")
        
        # Verifica se todos os dígitos são iguais
        if cpf == cpf[0] * 11:
            raise forms.ValidationError("CPF inválido.")
        
        # Validação do primeiro dígito verificador
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        resto = soma % 11
        if resto < 2:
            digito1 = 0
        else:
            digito1 = 11 - resto
        
        if int(cpf[9]) != digito1:
            raise forms.ValidationError("CPF inválido.")
        
        # Validação do segundo dígito verificador
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        resto = soma % 11
        if resto < 2:
            digito2 = 0
        else:
            digito2 = 11 - resto
        
        if int(cpf[10]) != digito2:
            raise forms.ValidationError("CPF inválido.")
        
        # Retorna o CPF formatado
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    
    # Validação para garantir que o número de jogos como titular não exceda o total
    def clean(self):
        cleaned_data = super().clean()
        jogos_total = cleaned_data.get('numeroTotalDeJogos')
        jogos_titular = cleaned_data.get('numeroDeJogosComoTitular')
        
        if jogos_total and jogos_titular and jogos_titular > jogos_total:
            raise forms.ValidationError("O número de jogos como titular não pode exceder o número total de jogos.")
        return cleaned_data

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, label='Nome')
    last_name = forms.CharField(max_length=30, required=True, label='Sobrenome')
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set better labels for password fields
        self.fields['password1'].label = 'Senha'
        self.fields['password2'].label = 'Confirmar Senha'
        
        # Add custom error messages
        self.fields['password2'].error_messages = {
            'required': 'Por favor, confirme sua senha.',
            'password_mismatch': 'As senhas não coincidem. Por favor, tente novamente.',
        }
        
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class UserLoginForm(forms.Form):
    username = forms.CharField(label='Usuário')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

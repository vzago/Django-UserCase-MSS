# Django UserCase MSS

## Início do Projeto

### Pré-requisitos
Certifique-se de que sua máquina atenda aos seguintes requisitos:
- Python instalado (versão 3.8 ou superior recomendada).
- Acesso à internet para clonar o repositório.

### Clonando o Repositório
Clone o repositório do GitHub com o seguinte comando no terminal ou prompt de comando:
```bash
git clone https://github.com/vzago/Django-UserCase-MSS.git
```

### Configurando o Ambiente Virtual
Depois de clonar o repositório, será necessário configurar um ambiente virtual para isolar as dependências do projeto.

1. **Criação do Ambiente Virtual:**
   Execute o seguinte comando no terminal na raiz do projeto:
   ```bash
   python -m venv venv
   ```

2. **Ativação do Ambiente Virtual:**
   - **Linux/MacOS:**
     ```bash
     source venv/bin/activate
     ```
   - **Windows (PowerShell):**
     ```powershell
     .\venv\Scripts\Activate
     ```
   - **Windows (Prompt de Comando):**
     ```cmd
     venv\Scripts\activate
     ```

> Após ativar o ambiente virtual, o nome do ambiente (como `venv`) deve aparecer antes do prompt.

### Instalando as Dependências
Com o ambiente virtual ativado, instale as dependências necessárias para o projeto:
```bash
pip install -r requirements.txt
```

### Configuração do Banco de Dados
1. **Gerar as Migrações:**
   Execute o comando abaixo para criar os scripts de migração:
   ```bash
   python manage.py makemigrations
   ```

2. **Aplicar as Migrações:**
   Para aplicar as migrações e configurar o banco de dados, execute:
   ```bash
   python manage.py migrate
   ```

### Executando o Servidor
Para iniciar o servidor de desenvolvimento, utilize o seguinte comando:
```bash
python manage.py runserver
```
O servidor estará acessível no endereço [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

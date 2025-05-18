# Etapa 1: imagem base com Python
# Use a imagem oficial do Python
FROM python:3.12-slim

# Configurar variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Definir o diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
COPY requirements.txt /app/
RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev-compat \
    libmariadb-dev \
    pkg-config

# Instalar dependências do Python
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install mysqlclient

# Criar diretório para arquivos estáticos
RUN mkdir -p /app/static

# Copiar os arquivos do projeto
COPY . /app/

# Comando para coletar arquivos estáticos
RUN python manage.py collectstatic --noinput

# Expor a porta para o Django
EXPOSE 8000

# Comando para rodar o servidor de desenvolvimento do Django
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:8000"]
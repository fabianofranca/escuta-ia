FROM python:3.10-slim

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    git \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Cria diretório da app
WORKDIR /app

# Copia arquivos
COPY . /app

# Instala dependências
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expõe porta padrão da Rasa
EXPOSE 5005

# Script de inicialização
CMD ["./start.sh"]

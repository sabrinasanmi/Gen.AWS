# Use a imagem base oficial do Python
FROM python:3.11-slim

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copie todo o código do projeto para o diretório de trabalho
COPY . .

# Defina a variável de ambiente para o Flask
ENV FLASK_APP=app.py

# Exponha a porta que o Flask vai usar
EXPOSE 5000

# Comando para iniciar o servidor Gunicorn para o Flask
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
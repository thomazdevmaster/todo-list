# Imagem base
FROM python:3.9-alpine

# Instalação do gunicorn (ideal para produção)
RUN pip install gunicorn

# Configura algumas opções de execução do interpretador Python
# Não gerar bytecode e desativar buffer de saída
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Busca os arquivos necessários
WORKDIR /app
COPY . /app

# Cria e configura um usuário não privilegiado dentro do contêiner
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# Subindo aplicação
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "todo:app"]

EXPOSE 5000

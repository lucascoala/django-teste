# 1º Estágio: Builder do backend Django + virtualenv
FROM python:3.11-slim AS builder

WORKDIR /app

ENV PIP_NO_CACHE_DIR=1 \
    PYTHONUNBUFFERED=1

# Instala dependências do sistema para compilação e conectores de banco
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    libpq-dev \
    libssl-dev \
    build-essential \
    netcat-traditional \
    libpango-1.0-0 \
    libharfbuzz0b \
    libpangoft2-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Instala ambiente virtual e dependências Python
COPY requirements.txt .
RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install virtualenv && \
    /venv/bin/pip install -r requirements.txt

# Copia o restante do código-fonte
COPY . .

# 2º Estágio: Builder do frontend
FROM node:18 AS frontend-builder

WORKDIR /frontend

# Copiar arquivos de dependência e instalar (melhor aproveitamento de cache)
COPY package*.json ./
RUN npm ci

# Copiar os arquivos estáticos e realizar o build (se necessário)
COPY ./static ./static
# RUN npm run build  # ativar se houver etapa de build

# 3º Estágio: Container final
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PATH="/venv/bin:$PATH"

# Instalar dependências nativas mínimas e dependências do WeasyPrint
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    netcat-traditional \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    libharfbuzz0b \
    libpangoft2-1.0-0 \
    libfreetype6 \
    libjpeg62-turbo \
    fonts-dejavu \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# Copiar virtualenv do builder
COPY --from=builder /venv /venv

# Copiar aplicação Django
COPY --from=builder /app /app

# Copiar assets do frontend
COPY --from=frontend-builder /frontend/static /app/static

# Coletar arquivos estáticos
RUN /venv/bin/python manage.py collectstatic --noinput

# Copiar o script de entrada e garantir permissão
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Criar usuário não-root
RUN addgroup --system appgroup && adduser --system --group appuser && \
    chown -R appuser:appgroup /app
USER appuser

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]

# Imagen base
FROM python:3.12-slim

# Instalar dependencias de sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc curl build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Instalar Poetry
ENV POETRY_VERSION=1.8.3
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos de Poetry
COPY pyproject.toml poetry.lock* /app/

# Instalar dependencias con Poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

# Copiar el proyecto completo
COPY . /app

# 🚀 IMPORTANTE: EXPOSE usa $PORT (Render lo inyecta)
EXPOSE $PORT

# 🚀 Comando de ejecución correcto para Render
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT"]

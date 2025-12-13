FROM python:3.11-slim

# System deps for mysqlclient
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire repo
COPY . /app

# 🔑 THIS IS THE KEY FIX
ENV PYTHONPATH=/app/school
ENV DJANGO_SETTINGS_MODULE=config.settings

CMD gunicorn config.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 1 \
    --threads 2 \
    --timeout 120

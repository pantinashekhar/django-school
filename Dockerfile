FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# We removed the MySQL dependencies (libmysqlclient-dev, gcc, etc.)
# We only need basic build tools just in case
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

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

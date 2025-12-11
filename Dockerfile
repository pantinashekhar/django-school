# Use official Python runtime as base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Set work directory
WORKDIR /app

# Install system dependencies (including MySQL client and dev headers for mysqlclient)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    pkg-config \
    default-mysql-client \
    default-libmysqlclient-dev \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project
COPY school/ .

# Create necessary directories
RUN mkdir -p /app/staticfiles /app/logs /app/media

# Expose port
EXPOSE 8000

# Run migrations, collect static files, and start gunicorn
CMD bash -c "python manage.py migrate && python manage.py collectstatic --noinput --clear && gunicorn --bind 0.0.0.0:8000 --workers 4 --timeout 120 school.wsgi:application"

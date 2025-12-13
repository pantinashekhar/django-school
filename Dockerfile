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

# Copy project correctly
COPY . /app

# Django environment variable
ENV DJANGO_SETTINGS_MODULE=school.settings

CMD ["gunicorn", "school.wsgi:application", "--bind", "0.0.0.0:8000"]

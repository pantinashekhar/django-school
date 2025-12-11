#!/bin/bash
set -e

# Wait for MySQL to be ready (if using MySQL)
if [ "$DB_ENGINE" = "mysql" ]; then
    echo "Waiting for MySQL to be ready..."
    while ! mysqladmin ping -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" --silent 2>/dev/null; do
        echo 'Waiting for MySQL...'
        sleep 2
    done
    echo "MySQL is ready!"
fi

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create logs directory
mkdir -p logs

# Start the application
echo "Starting Django application..."
exec "$@"


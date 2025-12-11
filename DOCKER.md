# Django School - Docker & Production Deployment Guide

## Quick Start (Development)

### Prerequisites
- Docker installed on your system
- Docker Compose installed

### Running with Docker Compose

1. **Clone and navigate to the project:**
```bash
cd django-school
```

2. **Copy environment file:**
```bash
cp .env.example .env
```

3. **Build and start containers:**
```bash
docker-compose up --build
```

The application will be available at `http://localhost:8000`

4. **Create a superuser (optional):**
```bash
docker-compose exec web python manage.py createsuperuser
```

5. **Access Django Admin:**
Navigate to `http://localhost:8000/admin`

## Development Docker Commands

**View logs:**
```bash
docker-compose logs -f web
```

**Run migrations:**
```bash
docker-compose exec web python manage.py migrate
```

**Access Django shell:**
```bash
docker-compose exec web python manage.py shell
```

**Stop containers:**
```bash
docker-compose down
```

**Stop and remove volumes:**
```bash
docker-compose down -v
```

**Rebuild containers:**
```bash
docker-compose build --no-cache
docker-compose up
```

## Production Deployment

### Prerequisites for Production
- Docker and Docker Compose installed on production server
- Domain name configured
- SSL certificate (Let's Encrypt recommended)
- Environment variables configured
- MySQL installed or Docker MySQL image available

### Production Setup with MySQL

1. **Copy production environment file:**
```bash
cp .env.example .env
```

2. **Update .env with production values:**
```bash
# Generate a new SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Edit .env with:
DEBUG=False
SECRET_KEY=<generated-secret-key>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# MySQL Configuration
DB_ENGINE=mysql
DB_NAME=school_db
DB_USER=school_user
DB_PASSWORD=<strong-random-password>
DB_HOST=db
DB_PORT=3306
MYSQL_ROOT_PASSWORD=<strong-mysql-root-password>

SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

3. **Build and run production containers with MySQL:**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

4. **Verify services are running:**
```bash
docker-compose -f docker-compose.prod.yml ps
docker-compose -f docker-compose.prod.yml logs -f
```

5. **Verify MySQL is connected:**
```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py dbshell
```

### Production Docker Commands

**View logs:**
```bash
docker-compose -f docker-compose.prod.yml logs -f web
docker-compose -f docker-compose.prod.yml logs -f db
```

**Execute migrations:**
```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
```

**Create superuser in production:**
```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

**Access MySQL:**
```bash
docker-compose -f docker-compose.prod.yml exec db mysql -u root -p school_db
```

**Stop containers:**
```bash
docker-compose -f docker-compose.prod.yml down
```

**Restart containers:**
```bash
docker-compose -f docker-compose.prod.yml restart
```

**Backup MySQL database:**
```bash
docker-compose -f docker-compose.prod.yml exec db mysqldump -u root -p school_db > backup.sql
```

**Restore MySQL database:**
```bash
docker-compose -f docker-compose.prod.yml exec -T db mysql -u root -p school_db < backup.sql
```

## Building Docker Image Manually

### Build the Docker image:
```bash
docker build -t django-school:latest .
docker build -t django-school:1.0 .  # With version tag
```

### Tag for Docker Hub (optional):
```bash
docker tag django-school:latest yourusername/django-school:latest
docker push yourusername/django-school:latest
```

### Run the container manually:
```bash
docker run -p 8000:8000 \
  -e DEBUG=False \
  -e SECRET_KEY=your-secret-key \
  -e ALLOWED_HOSTS=localhost \
  -v $(pwd)/school:/app \
  django-school:latest
```

## Project Structure
```
django-school/
├── Dockerfile                  # Production image definition
├── docker-compose.yml          # Development orchestration
├── docker-compose.prod.yml     # Production orchestration
├── .dockerignore               # Files excluded from Docker build
├── docker-entrypoint.sh        # Container startup script
├── .env.example                # Example environment variables
├── .gitignore                  # Git ignore patterns
├── requirements.txt            # Python dependencies
├── school/                     # Django project directory
│   ├── manage.py
│   ├── db.sqlite3
│   ├── school/                # Project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   └── core/                  # Django app
├── DOCKER.md                   # This file
└── README.md
```

## Environment Variables

### Development (.env)
```
DEBUG=False
SECRET_KEY=django-insecure-key
ALLOWED_HOSTS=localhost,127.0.0.1,web
DJANGO_SETTINGS_MODULE=school.settings
DB_ENGINE=sqlite3
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
DJANGO_LOG_LEVEL=INFO
```

### Production (.env) - MySQL Configuration
```
DEBUG=False
SECRET_KEY=<strong-random-key>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DJANGO_SETTINGS_MODULE=school.settings

# MySQL Configuration
DB_ENGINE=mysql
DB_NAME=school_db
DB_USER=school_user
DB_PASSWORD=<strong-password>
DB_HOST=db
DB_PORT=3306
MYSQL_ROOT_PASSWORD=<strong-mysql-root-password>

SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
DJANGO_LOG_LEVEL=WARNING
```

## Security Checklist for Production

- [ ] Change SECRET_KEY to a strong random value
- [ ] Set DEBUG=False
- [ ] Update ALLOWED_HOSTS with your domain
- [ ] Enable SSL/HTTPS (SECURE_SSL_REDIRECT=True)
- [ ] Set SESSION_COOKIE_SECURE=True
- [ ] Set CSRF_COOKIE_SECURE=True
- [ ] Use strong database credentials for MySQL
- [ ] Set up proper logging (logs stored in /app/logs)
- [ ] Configure backup strategy for MySQL database (daily backups recommended)
- [ ] Set up monitoring and health checks
- [ ] Keep Docker images updated
- [ ] Use secrets management for sensitive data
- [ ] Regular MySQL maintenance and optimization

## Database Configuration: SQLite vs MySQL

### Development (SQLite - Default)
- No additional setup required
- Suitable for local development and testing
- Database file: `school/db.sqlite3`

### Production (MySQL - Recommended)
- Set `DB_ENGINE=mysql` in .env
- Run with: `docker-compose -f docker-compose.prod.yml up`
- Automatically includes MySQL service
- Better performance and scalability
- Supports concurrent users better

### Switch from SQLite to MySQL
1. **In development, keep using SQLite** (set DB_ENGINE=sqlite3)
2. **In production, use MySQL** (set DB_ENGINE=mysql in .env)
3. **Migrate data** (if moving existing data):
   ```bash
   # Export from SQLite
   python manage.py dumpdata > data.json
   
   # On MySQL instance, import data
   python manage.py loaddata data.json
   ```

## Nginx Reverse Proxy Setup (Optional)

Create `nginx.conf`:
```nginx
upstream django {
    server web:8000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    client_max_body_size 10M;

    location / {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /app/staticfiles/;
    }

    location /media/ {
        alias /app/media/;
    }
}
```

Add to docker-compose.prod.yml:
```yaml
  nginx:
    image: nginx:latest
    container_name: django-school-nginx
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "80:80"
    depends_on:
      - web
    networks:
      - web-network
```

## Database Upgrade (PostgreSQL)

To upgrade from SQLite to PostgreSQL in production:

1. Install PostgreSQL driver:
```bash
pip install psycopg2-binary
```

2. Update settings.py DATABASES:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'school'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

3. Add PostgreSQL service to docker-compose.prod.yml

## Troubleshooting

**Port already in use:**
```bash
docker-compose down
# Or change port in docker-compose.yml
docker run -p 8001:8000 ...
```

**Database issues:**
```bash
docker-compose down -v
docker-compose up --build
```

**MySQL Connection Issues:**
```bash
# Check MySQL logs
docker-compose -f docker-compose.prod.yml logs db

# Test MySQL connection
docker-compose -f docker-compose.prod.yml exec db mysql -u root -p -e "SELECT 1"

# Verify Django can connect
docker-compose -f docker-compose.prod.yml exec web python manage.py dbshell
```

**MySQL Service Fails to Start:**
```bash
# Remove and recreate MySQL volume
docker-compose -f docker-compose.prod.yml down -v
docker-compose -f docker-compose.prod.yml up -d db
docker-compose -f docker-compose.prod.yml logs db
```

**Permission denied on docker-entrypoint.sh:**
```bash
chmod +x docker-entrypoint.sh
```

**Migrations not running:**
```bash
docker-compose exec web python manage.py migrate --verbosity 3
```

**Static files not loading:**
```bash
docker-compose exec web python manage.py collectstatic --noinput --clear
```

**Container won't start:**
```bash
docker logs <container_id>
docker-compose logs web
```

## MySQL Database Management

### Backup MySQL Database
```bash
# Create backup
docker-compose -f docker-compose.prod.yml exec db mysqldump -u root -p$MYSQL_ROOT_PASSWORD school_db > backup_$(date +%Y%m%d_%H%M%S).sql

# View backups
ls -lh backup_*.sql
```

### Restore MySQL Database
```bash
# Restore from backup
docker-compose -f docker-compose.prod.yml exec -T db mysql -u root -p$MYSQL_ROOT_PASSWORD school_db < backup_20241210_143022.sql
```

### MySQL Maintenance
```bash
# Access MySQL shell
docker-compose -f docker-compose.prod.yml exec db mysql -u root -p

# Show databases
mysql> SHOW DATABASES;

# Show database size
mysql> SELECT table_schema "DB Name", ROUND(SUM(data_length+index_length)/1024/1024, 2) "Size (MB)" FROM information_schema.tables WHERE table_schema != "information_schema" GROUP BY table_schema;

# Create user backup
docker-compose -f docker-compose.prod.yml exec db mysqldump -u root -p$MYSQL_ROOT_PASSWORD --no-data school_db > schema_backup.sql
```

## Performance Optimization

1. **Increase workers based on CPU cores:**
```dockerfile
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "8", "school.wsgi:application"]
```

2. **Enable caching:**
```python
# Add to settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
```

3. **Database connection pooling** (when using MySQL):
```bash
pip install django-db-connection-pool
```

Then add to settings.py:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django_db_conn_pool.mysql',
        'CONN_MAX_AGE': 600,
        'OPTIONS': {
            'MAX_CONNS': 20
        }
    }
}
```

4. **Static file compression:**
```bash
pip install whitenoise
```

## Monitoring & Logging

Logs are stored in `/app/logs/django.log`. Configure log rotation and monitoring as per your infrastructure requirements.

Monitor container health:
```bash
docker stats
docker-compose logs -f web
```

## Notes

- Your original codebase in `school/` directory remains unchanged
- Development uses SQLite; upgrade to PostgreSQL for production
- All sensitive data should be in environment variables
- Regular backups recommended for database
- Keep Docker images and dependencies updated


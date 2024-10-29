#!/bin/sh

# Set defaults if not provided
RED_HOST=${REDIS_HOST:-redis}
RED_PORT=${REDIS_PORT:-6379}
DB_HOST=${DATABASE_HOST:-db}
DB_PORT=${DATABASE_PORT:-5432}

# Wait for Redis to be ready
echo "Waiting for Redis at $RED_HOST:$RED_PORT..."
while ! nc -z "$RED_HOST" "$RED_PORT"; do
    sleep 0.1
done
echo "Redis is up"

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL at DB_HOST:$DB_PORT..."
while ! nc -z "$DB_HOST" "$DB_PORT"; do
    sleep 0.1
done
echo "PostgreSQL is up"

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

if [ -n "$CREATE_SUPERUSER" ]; then
  echo "Creating superuser: $DJANGO_SUPERUSER_USERNAME"
  python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL
else
  echo "$CREATE_SUPERUSER variable is not set. Skipping superuser creation."
fi

if [ -z "$@" ]; then
    echo "Running the default command...For render deployment"
    exec gunicorn STCGApi.wsgi:application --bind 0.0.0.0:8000 --workers 4
else
    exec "$@"
fi

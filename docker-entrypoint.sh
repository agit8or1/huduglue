#!/bin/bash
# HuduGlue Docker Entrypoint Script

set -e

echo "HuduGlue Docker Container Starting..."

# Wait for database to be ready
echo "Waiting for database..."
while ! python -c "import MySQLdb; MySQLdb.connect(host='${DB_HOST}', user='${DB_USER}', passwd='${DB_PASSWORD}', db='${DB_NAME}')" 2>/dev/null; do
    echo "Database is unavailable - sleeping"
    sleep 2
done

echo "Database is ready!"

# Run migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if env variables are set
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ]; then
    echo "Creating superuser..."
    python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD');
    print('Superuser created successfully');
else:
    print('Superuser already exists');
" || echo "Superuser creation skipped or failed"
fi

echo "Starting application..."

# Execute the main command
exec "$@"

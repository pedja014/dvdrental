#!/bin/bash

echo "Waiting for PostgreSQL to be ready..."
attempt=0
max_attempts=60

while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
  attempt=$((attempt + 1))
  if [ $attempt -gt $max_attempts ]; then
    echo "ERROR: PostgreSQL did not become ready in time"
    exit 1
  fi
  echo "Attempt $attempt/$max_attempts - waiting for database..."
  sleep 2
done
echo "PostgreSQL is ready!"

# Wait a bit more for database initialization
echo "Waiting for database initialization..."
sleep 10

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Run migrations
echo "Running migrations..."
python manage.py makemigrations --noinput || echo "No new migrations to create"
python manage.py migrate --noinput || {
    echo "ERROR: Migrations failed"
    echo "This might be because the database is still initializing"
    echo "Waiting 30 more seconds..."
    sleep 30
    python manage.py migrate --noinput || exit 1
}

# Create superuser if it doesn't exist (parameterized via env vars)
echo "Creating superuser..."
python manage.py shell << END || echo "Superuser creation skipped"
from django.contrib.auth import get_user_model
import os

User = get_user_model()

admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
admin_email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')
admin_role = os.environ.get('ADMIN_ROLE', 'admin')

try:
    if not User.objects.filter(username=admin_username).exists():
        # CustomUser expects a role field; default to env-provided role
        User.objects.create_superuser(admin_username, admin_email, admin_password, role=admin_role)
        print(f"Superuser created: username={admin_username}")
    else:
        print('Superuser already exists')
except Exception as e:
    print(f'Error creating superuser: {e}')
END

# Execute the main command
exec "$@"


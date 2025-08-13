#!/bin/sh

# O shell irá encerrar a execução do script quando um comando falhar
set -e

echo "🟡 Starting Django application setup..."

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "🔄 Running database migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "🚀 Starting Django development server..."
python manage.py runserver 0.0.0.0:8000
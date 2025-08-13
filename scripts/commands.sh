#!/bin/sh

# O shell irá encerrar a execução do script quando um comando falhar
set -e

echo "🟡 Using SQLite database - no external database connection needed"

# SQLite database will be created automatically when migrations run
echo "✅ SQLite Database Ready"

python manage.py collectstatic --noinput --clear
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py runserver 0.0.0.0:8000
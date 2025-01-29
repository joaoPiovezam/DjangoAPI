#!/bin/sh

# O shell irá encerrar a execução do script quando um comando falhar
set -e

while ! nc -z jp-db.c1y6wwic8wtz.sa-east-1.rds.amazonaws.com 5432; do
  echo "🟡 Waiting for Postgres Database Startup (jp-db.c1y6wwic8wtz.sa-east-1.rds.amazonaws.com 5432) ..."
  sleep 2
done

echo "✅ Postgres Database Started Successfully ($POSTGRES_HOST:$POSTGRES_PORT)"

#python manage.py collectstatic --noinput --clear
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py runserver 0.0.0.0:8000
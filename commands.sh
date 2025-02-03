echo "colentadno"
python /venv/bin/ manage.py collectstatic --noinput
echo "coletado"
python /venv/bin/ manage.py migrate --noinput
echo "migrado"
#python -m gunicorn --bind 0.0.0.0:8000 --workers 3 setup.wsgi:application
python  manage.py runserver 0.0.0.0:80
echo "rodando"
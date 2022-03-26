release: python manage.py migrate
web: gunicorn backend.wsgi --log-file=-

web: waitress-serve --port=8000 backend.wsgi:application
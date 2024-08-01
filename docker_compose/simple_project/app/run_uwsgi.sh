#!/usr/bin/env bash

set -e

python manage.py migrate
python manage.py collectstatic --noinput
python manage.py compilemessages

if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    python manage.py createsuperuser --noinput || true
fi

chown www-data:www-data /var/log
uwsgi --strict --ini /etc/app/uwsgi.ini

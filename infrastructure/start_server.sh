#!/usr/bin/env sh

# start-server.sh
cd /opt/app

. venv/bin/activate

cd church_cms

if [ "$APP_ENV" != "prod" ]; then
  python manage.py migrate
fi


if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] && [ "$APP_ENV" != "prod" ] ; then
    python manage.py createsuperuser --no-input
    python manage.py collectstatic --no-input --clear
fi

python manage.py collectstatic --no-input --clear

gunicorn church_cms.wsgi --bind 0.0.0.0:8000 --workers 3

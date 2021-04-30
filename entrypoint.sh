#!/bin/sh

python manage.py migrate --no-input
python manage.py collectstatic --no-input

uwsgi --socket :8000 --master --enable-threads --module bank_project.wsgi
#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Comment out and run manually with
# $ docker-compose exec web python manage.py flush --no-input
# $ docker-compose exec web python manage.py migrate
python manage.py flush --no-input
python manage.py migrate

exec "$@"
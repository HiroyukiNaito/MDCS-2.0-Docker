#!/bin/bash
# Wait for mongodb
until nc -z mongo.svc 27017; do
    echo "=> $(date) - Waiting for confirmation of MongoDB service startup"
    sleep 1
done

# Wait for PostgreSQL
until nc -z psql.svc 5432; do
    echo "=> $(date) - Waiting for confirmation of PostgreSQL service startup"
    sleep 1
done

echo "  ---------------------Start celery-----------------------"
rm -f *.pid
celery multi start -A mdcs worker -l info -Ofair --purge
chmod 777 ./worker.log

# Wait for celery
until celery -A mdcs status 2>/dev/null; do
	echo "=> $(date) - Waiting for confirmation of Celery service startup"
 	sleep 1
done

# Migrate/superuser
python manage.py migrate auth
python manage.py migrate

# Collectstatic
python manage.py collectstatic --noinput
python manage.py compilemessages

# Superuser Create
echo "from django.contrib.auth.models import User; User.objects.create_superuser('mgi_superuser', 'user_email@institution.com', 'mgi_superuser_pwd')" | python manage.py shell

# Start Django
echo "  ----------------------Start Django-----------------------"
# uwsgi --socket mysite.sock --chdir /srv/mgi-mdcs/ --wsgi-file /srv/mgi-mdcs/mdcs/wsgi.py --chmod-socket=666
python manage.py runserver 0.0.0.0:8000
echo "Started"

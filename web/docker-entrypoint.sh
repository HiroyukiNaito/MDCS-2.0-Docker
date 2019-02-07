#!/bin/bash

# Wait for postgres
until nc -z postgres 5432; do
    echo "=> $(date) - Waiting for confirmation of Postgres service startup"
    sleep 1
done

# Wait for mongodb
until nc -z db_mongo 27017; do
    echo "=> $(date) - Waiting for confirmation of MongoDB service startup"
    sleep 1
done

echo "  ---------------------Start celery-----------------------"
rm -f *.pid
celery multi start -A mdcs worker -l info -Ofair --purge
chmod 777 ./worker.log
su -m myuser -c "celery multi start -A mdcs worker -l info -Ofair --purge"

# Wait for celery
until celery -A mdcs status 2>/dev/null; do
	echo "=> $(date) - Waiting for confirmation of Celery service startup"
 	sleep 1
done

# Migrate/superuser
python manage.py migrate auth
python manage.py migrate
#echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | ./manage.py shell
# Collectstatic
python manage.py collectstatic --noinput
    
# Start Django
echo "  ----------------------Start Django-----------------------"
# uwsgi --socket mysite.sock --chdir /srv/mgi-mdcs/ --wsgi-file /srv/mgi-mdcs/mdcs/wsgi.py --chmod-socket=666
# uwsgi --wsgi-file /srv/mgi-mdcs/mdcs/wsgi.py --static-map /static=./static --http 0.0.0.0:8000
python manage.py runserver 0.0.0.0:8000
echo Started

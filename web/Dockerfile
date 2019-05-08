############################################################
# Dockerfile to run a Django-based web application
# Based on an Ubuntu Image
############################################################

# Set the base image to use to Ubuntu
FROM ubuntu:16.04

# Set the file maintainer (your name - the file's author)
LABEL maintainer="Hiroyuki Naito, National Institute for Materials Science"

# Set env variables used in this Dockerfile (add a unique prefix, such as DOCKYARD)
# Directory in container for project source files
ENV DOCKYARD_SRVPROJ=/srv/mgi-mdcs
# Git repository
ENV GIT_REPO=https://github.com/usnistgov/MDCS.git

# Update the default application repository sources list
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y python python-pip
RUN apt-get install -y libxml2-dev libxslt-dev python-dev lib32z1-dev
RUN apt-get install -y curl python
RUN curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
RUN python get-pip.py
RUN apt-get -y install git
RUN apt-get -y install python-psycopg2
RUN apt-get -y install netcat
RUN apt-get -y install gettext


# Git clone
RUN git clone --branch 2.0.1 $GIT_REPO $DOCKYARD_SRVPROJ

# Mongoengine
RUN git clone --branch v0.2.1 "https://github.com/MongoEngine/django-mongoengine.git"
RUN cd django-mongoengine && pip install .


# Install Python dependencies

RUN python -m pip install --upgrade pip
RUN pip install -r $DOCKYARD_SRVPROJ/requirements.txt
RUN pip install -r $DOCKYARD_SRVPROJ/requirements.core.txt
RUN pip install redis==3.2.0

# Install uwsgi
RUN pip install uwsgi

# Copy entrypoint script into the image
WORKDIR $DOCKYARD_SRVPROJ
COPY ./docker-entrypoint.sh /srv/mgi-mdcs/
RUN chmod +x /srv/mgi-mdcs/docker-entrypoint.sh

# Download XSD
RUN git clone --branch master "https://github.com/MDCS-community/modular-data-models-include.git"

# Port to expose
EXPOSE 8000

# Create unprivileged user
RUN adduser --disabled-password --gecos '' myuser

# User change
RUN chown myuser:myuser -R $DOCKYARD_SRVPROJ
USER myuser
RUN chmod 700 $DOCKYARD_SRVPROJ

ENTRYPOINT ["/srv/mgi-mdcs/docker-entrypoint.sh"]

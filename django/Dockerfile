# This file is part of the research.fi API service
#
# Copyright 2019 Ministry of Education and Culture, Finland
#
# :author: CSC - IT Center for Science Ltd., Espoo Finland servicedesk@csc.fi
# :license: MIT

# Use official Python image as base. https://hub.docker.com/_/python
FROM python:3.6-alpine

# Set Python environment variables
#   PYTHONDONTWRITEBYTECODE: Do not try to write .pyc files on the import of source modules.
#   PYTHONUNBUFFERED: Force the stdout and stderr streams to be unbuffered.
# https://docs.python.org/3/using/cmdline.html#environment-variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create non-root user 'appuser' and group 'appgroup'.
# Python environment and application code are installed into
# and executed from user's home directory /home/appuser.
#
# Since adding a new user always produces the same result, it should be
# executed before software installations. The result is cached as a Docker layer.
RUN addgroup -S appgroup && adduser -S appuser -G appgroup -u 1000

# Install pip and pipenv.
# https://pypi.org/project/pip/
# https://github.com/pypa/pipenv
RUN pip install --upgrade pip
RUN pip install pipenv

# Change user to 'appuser'. Non-root user allows container
# to be used in OpenShift environment.
USER appuser
WORKDIR /home/appuser

# Copy Pipfile into container.
COPY ./Pipfile /home/appuser/Pipfile

 # Install Python packages specified in Pipfile
RUN pipenv install --deploy --ignore-pipfile

# Copy Django application code into container.
COPY ./webapps /home/appuser/webapps

ENV PYTHONPATH="/home/appuser/webapps:${PYTHONPATH}"
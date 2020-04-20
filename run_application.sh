#!/bin/bash

echo -e "Starting Application ..."

cd ./fashion/

pipenv run python manage.py runserver

echo -e "Application Stopped..."
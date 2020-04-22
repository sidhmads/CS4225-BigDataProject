#!/bin/bash

echo -e "Migrate Data To Elastic ..."

cd ./fashion/

pipenv run python setupelastic.py
#!/bin/bash

echo -e "Starting Elastic Service ..."

cd ./fashion/

elasticsearch

python setupelastic.py

logstash -f logstash.conf
#!/bin/bash

echo -e "Partitioning the images"

python partition.py

echo -e "Normalizing the images"

python normalize.py

echo -e "Converting images to grey scale"

python greyscale.py
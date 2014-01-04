#!/bin/bash
##
## setup script for this repo
## virtualenv must be installed
##

virtualenv --no-site-packages ./env
./env/bin/pip install --upgrade -r ./requirements.txt


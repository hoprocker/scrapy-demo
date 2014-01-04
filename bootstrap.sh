#!/bin/bash
##
## setup script for this repo
## virtualenv must be installed
##

apt-get install -y python2.7 python2.7-dev redis-server python-pip libxml2-dev libxslt-dev libssl-dev lib32z1-dev
## change 'lib32z1-dev' to 'zlib1g-dev' for 32-bit
pip install virtualenv
virtualenv --no-site-packages ./env
./env/bin/pip install --upgrade -r ./requirements.txt


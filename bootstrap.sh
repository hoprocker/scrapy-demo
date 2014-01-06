#!/bin/bash
##
## setup script for this repo
##

apt-get install -y python2.7 python2.7-dev redis-server python-pip libxml2-dev libxslt-dev libssl-dev scrapyd lib32z1-dev
## change 'lib32z1-dev' above to 'zlib1g-dev' for 32-bit
pip install --upgrade -r ./requirements.txt
cp ./scrapyd.conf /etc/scrapyd/scrapyd.conf
curl http://localhost:6800/delproject.json -d project=realtortest
/bin/bash activate
pushd realtortest && scrapyd-deploy scrapyd -p realtortest && popd

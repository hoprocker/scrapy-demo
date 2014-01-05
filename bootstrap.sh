#!/bin/bash
##
## setup script for this repo
##

curl -s http://archive.scrapy.org/ubuntu/archive.key | apt-key add - ## get GPG key
echo "deb http://archive.scrapy.org/ubuntu saucy main" > /etc/apt/sources.list.d/scrapy.list
apt-get update
apt-get install -y python2.7 python2.7-dev redis-server python-pip libxml2-dev libxslt-dev libssl-dev scrapyd lib32z1-dev
## change 'lib32z1-dev' above to 'zlib1g-dev' for 32-bit
pip install virtualenv
virtualenv --no-site-packages ./env
./env/bin/pip install --upgrade -r ./requirements.txt
chown -R ubuntu /www
cp ./scrapyd.conf /etc/scrapyd/scrapyd.conf
curl http://localhost:6800/delproject.json -d project=realtortest
/bin/bash ./env/bin/activate
pushd realtortest && ../env/bin/scrapyd-deploy scrapyd -p realtortest && popd

#!/bin/bash
USER=ubuntu
SERVER=54.200.177.70
ROOT="/www"   ## no trailing slash

echo "deploying code"
echo ""
ssh $USER@$SERVER "sudo mkdir -p $ROOT && sudo chown -R $USER $ROOT"
rsync -axv --delete --ignore-errors --exclude ".git" --exclude "env" ~/dev/scrapy-test/ $USER@$SERVER:$ROOT/

echo "killing old processes"
echo ""
ssh $USER@$SERVER "sudo /bin/netstat -alpn | grep 9097 | awk '{print \$7}' | grep python | sed -e 's/\/python//' | sudo xargs kill"
ssh $USER@$SERVER "pushd $ROOT && sudo /bin/bash ./bootstrap.sh"
ssh $USER@$SERVER "sudo chown -R $USER $ROOT"
ssh $USER@$SERVER "pushd $ROOT && $ROOT/env/bin/python $ROOT/main.py &"

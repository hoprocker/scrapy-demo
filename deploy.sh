#!/bin/bash
USER=ubuntu
SERVER=54.200.177.70
ROOT="/www"   ## no trailing slash

rsync -axv --delete --ignore-errors --exclude ".git" --exclude "env" ~/dev/scrapy-test/ $USER@$SERVER:$ROOT/
ssh $USER@$SERVER "pushd $ROOT && . ./env/bin/activate && sudo /bin/bash ./bootstrap.sh"
ssh $USER@$SERVER "pushd $ROOT && $ROOT/env/bin/python $ROOT/main.py"

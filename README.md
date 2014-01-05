# what this is
A simple demonstration of [scrapy](http://scrapy.org/) and [Flask](http://flask.pocoo.org/). Downloads some data from realtor.com, stores it in [Redis](http://redis.io), and makes it available on a simple flask website. *DOES* overwrite system variables, so use virtualization (a fine candidate for a [Docker](http://docker.io) container!).

* NOTE this kills whatever is running on port 9097!!!
* NOTE this application makes *global* changes! Run virtualized!

# Tested with
AWS stock Ubuntu 13:10 image, 64-bit (can work w/ 32-bit also, check bootstrap.sh)

# deployment
* pull down the code locally
* edit the variables at the top of `deploy.sh`
* make sure that you can 'sudo' w/ the user on the remote machine
* run `./deploy.sh`
* check out the page on `http://insert-ip:9097`

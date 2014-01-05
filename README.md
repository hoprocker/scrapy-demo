# what this is
A simple demonstration of scrapy and Flask. Downloads some data from realtor.com, stores it in Redis, and makes it available on a simple flask website. *DOES* overwrite system variables, so use virtualization (a fine candidate for a Docker container!).

Very generic right now, just stores every listing as a hash in a Redis database and pulls it every time.

* NOTE this kills whatever is running on port 9097!!!
* NOTE this application makes *global* changes! Run virtualized!

# Tested with
AWS stock Ubuntu 13:10 image, 64-bit (can work w/ 32-bit also, check bootstap.sh)

# deployment
* pull down the code locally
* edit the variables at the top of `deploy.sh`
* make sure that you can 'sudo' w/ the user on the remote machine
* run `./deploy.sh`
* check out the page on http://localhost:9097

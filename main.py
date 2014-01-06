"""
a simple web interface which displays some information about the jobs
and the data retrieved.

available at http://localhost;9097
"""
from flask import Flask, make_response, render_template, request, redirect, url_for, flash, get_flashed_messages
import json
from realtortest.realtortest.db import datastore
import requests

app = Flask(__name__)
app.secret_key = "hi there"

@app.route("/")
def index():
    project="realtortest"
    stats = get_scrapyd_stat(project)
    data = datastore.list()
    [d.update({"per_sqft":float(d["price"])/float(d["sqft"])}) for d in data]
    return render_template("main.html",
            data=data,
            job_id=get_flashed_messages(),
            fields=datastore.list()[0].keys(),
            **stats)

@app.route("/schedule")
def schedule():
    res = json.loads(requests.post("http://localhost:6800/schedule.json", {"project":"realtortest", "spider":"realtor"}).content)
    if res['status'] == "ok":
        job_id = res["jobid"]
    else:
        job_id = "FAIL"
    flash(job_id)
    return redirect(url_for('index'))

def get_scrapyd_stat(project, host="localhost", port=6800):
    base = "http://%s:%d" % (host, port)
    stats = {"project":project,
        "projects":requests.get("%s/listprojects.json" % base).content,
        "spiders":requests.get("%s/listspiders.json?project=%s" % (base,project)).content,
        "jobs":requests.get("%s/listjobs.json?project=%s" % (base,project)).content,}
    stats.update(aggregate_stats())
    return stats

def aggregate_stats():
    """
    a simple, contrived example of using our (very inefficient) datastore
    to glean some insight into the data

    admittedly, there's a *lot* of very inefficient work here!
    """
    allstats = datastore.list()  ## just get it all
    p_types = set()
    for stat in allstats:
        p_types.add(stat["property_type"])
    price_sqft = {"all":[float(p["price"])/float(p["sqft"]) for p in allstats]}
    price_sqft.update({"mean":sum(price_sqft["all"])/len(price_sqft["all"]),
                        "med":price_sqft["all"][int(len(price_sqft["all"])/2)]})
    #price_bath = {"all":[float(p["price"])/float(p["baths"]) for p in allstats]}
    #price_bath.update({"mean":sum(price_bath["all"])/len(price_bath["all"]),
                        #"med":price_bath["all"][int(len(price_bath["all"])/2)]})

    return {"types":list(p_types),
            "price_sqft":price_sqft,
            #"price_bed":price_bed,
            #"price_bath":price_bath,
            }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9097, debug=True)

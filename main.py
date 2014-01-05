from flask import Flask, make_response, render_template, request, redirect, url_for, flash, get_flashed_messages
import json
from realtortest.realtortest.db import datastore
import requests

app = Flask(__name__)
app.debug = True
app.secret_key = "hi there"

@app.route("/")
def index():
    project="realtortest"
    stats = get_scrapyd_stat(project)
    return render_template("main.html",
            data=datastore.list(),
            job_id=get_flashed_messages(),
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
    return {"project":project,
        "projects":requests.get("%s/listprojects.json" % base).content,
        "spiders":requests.get("%s/listspiders.json?project=%s" % (base,project)).content,
        "jobs":requests.get("%s/listjobs.json?project=%s" % (base,project)).content,}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9097, debug=True)

from flask import render_template, redirect, url_for

from app import app


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/queues')
def queues():
    return render_template('queues.html')


@app.route('/workers')
def workers():
    return render_template('workers.html')


@app.route('/jobs')
def jobs():
    return render_template('jobs.html')


@app.route('/schedulers')
def schedulers():
    return render_template('schedulers.html')
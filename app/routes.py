from flask import current_app, render_template, redirect, url_for

from app import app


def _get_queue_list():
    rq_queues = current_app.config.get("RQ_QUEUES")

    if rq_queues.find(",") >= 0:
        return rq_queues.split(",")
    else:
        return [rq_queues]


@app.route('/')
@app.route('/index')
def index():
    rq_queues = _get_queue_list()
    rq_workers = _get_queue_list()
    return render_template('index.html', rq_queues=rq_queues, rq_workers=rq_workers)


@app.route('/queues')
def queues():
    rq_queues = _get_queue_list()
    return render_template('queues.html', rq_queues=rq_queues)


@app.route('/workers')
def workers():
    rq_workers = _get_queue_list()
    return render_template('workers.html', rq_workers=rq_workers)


@app.route('/jobs')
def jobs():
    return render_template('jobs.html')


@app.route('/schedulers')
def schedulers():
    return render_template('schedulers.html')
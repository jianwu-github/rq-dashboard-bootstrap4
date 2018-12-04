from flask import current_app, render_template, redirect, url_for

from redis import Redis
from rq import Queue

from app import app


def _get_queue_list():
    rq_queues = current_app.config.get("RQ_QUEUES")

    if rq_queues.find(",") >= 0:
        return rq_queues.split(",")
    else:
        return [rq_queues]
    
 
def _get_job_list(redis_conn):
    queue_list = _get_queue_list()
    job_list = []
    
    # TODO pull jobs from queues
    for q in queue_list:
        queue = Queue(q, connection=redis_conn)
        jobs = queue.get_jobs()
        
        for j in jobs:
            job_list.append({'id': j.get_id(), 'status': j.get_status()})
    
    return job_list


@app.route('/')
@app.route('/index')
def index():
    rq_queues = _get_queue_list()
    rq_workers = _get_queue_list()
    job_list = _get_job_list(current_app.redis_conn)
    return render_template('index.html', rq_queues=rq_queues, rq_workers=rq_workers, job_list=job_list)


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
    job_list = _get_job_list(current_app.redis_conn)
    return render_template('jobs.html', job_list=job_list)


@app.route('/schedulers')
def schedulers():
    return render_template('schedulers.html')

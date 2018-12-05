from flask import current_app, render_template

from rq import Queue
from rq.job import Job
from rq.registry import FinishedJobRegistry

from rq_scheduler import Scheduler

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

    for q in queue_list:
        queue = Queue(q, connection=redis_conn)
        jobs = queue.get_jobs()

        for j in jobs:
            job_list.append({'id': j.get_id(), 'status': j.get_status()})

        registry = FinishedJobRegistry(name=q, connection=redis_conn)
        job_ids = registry.get_job_ids()

        for jid in job_ids:
            job = Job.fetch(jid, connection=redis_conn)
            job_list.append({'id': jid, 'status': job.get_status()})

    return job_list


def _get_scheduled_jobs(redis_conn):
    queue_list = _get_queue_list()
    job_list = []

    for q in queue_list:
        scheduler = Scheduler(queue_name=q, connection=redis_conn)
        jobs = scheduler.get_jobs()

        for j in jobs:
            job_list.append({'id': j.get_id(), 'status': j.get_status()})

    return job_list


def _get_scheduler_sts(redis_conn):
    queue_list = _get_queue_list()
    scheduler_list = []

    for q in queue_list:
        scheduler = Scheduler(queue_name=q, connection=redis_conn)

        if (scheduler.connection.exists(scheduler.scheduler_key) and
            not scheduler.connection.hexists(scheduler.scheduler_key, 'death')):
            scheduler_list.append({'id': f'scheduler on {q}', 'status': 'running'})
        else:
            scheduler_list.append({'id': f'No running scheduler on {q}', 'status': 'N/A'})

    return scheduler_list


@app.route('/')
@app.route('/index')
def index():
    rq_queues = _get_queue_list()
    rq_workers = _get_queue_list()
    job_list = _get_job_list(current_app.redis_conn)
    schedulers = _get_scheduler_sts(current_app.redis_conn)
    return render_template('index.html', rq_queues=rq_queues, rq_workers=rq_workers, job_list=job_list, schedulers=schedulers)


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
    schedulers = _get_scheduler_sts(current_app.redis_conn)
    return render_template('schedulers.html', schedulers=schedulers, scheduled_jobs=scheduled_jobs)

from flask import current_app, url_for

from rq import (Queue, Worker, cancel_job, get_failed_queue, pop_connection, push_connection, requeue_job)
from rq.job import Job
from rq_scheduler import Scheduler


from app import app


@app.before_first_request
def setup_rq_connection():
    redis_host = current_app.config.get("REDIS_HOST")
    redis_port = current_app.config.get("REDIS_PORT")
    redis_db = current_app.config.get("REDIS_DB")
    queue_list = current_app.config.get("RQ_QUEUES")

    print(f'connecting to Redis {redis_host}:{redis_port}/{redis_db}')
    print(f'monitoring a list of queue: {queue_list}')


@app.before_request
def prepare_rq_connection():
    pass


@app.teardown_request
def release_rq_connection(exception=None):
    pass



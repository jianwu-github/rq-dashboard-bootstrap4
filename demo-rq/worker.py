import os

from pathlib import Path
from random import randrange

from dotenv import load_dotenv
from redis import Redis
from rq import Connection, Worker

# import required job packages/modules

worker_prj_dir = Path(__file__).parent.absolute().parent
worker_prj_env_file = worker_prj_dir / 'rq-worker.env'

if worker_prj_env_file.exists():
    print(f'Running local dev env, and loading environment variables from file: {worker_prj_env_file}')
    load_dotenv(worker_prj_env_file)
else:
    print(f'Running in docker, no rq-worker env file: {worker_prj_env_file}')

_redis_host = os.environ.get("REDIS_HOST")
_redis_port = os.environ.get("REDIS_PORT")
_redis_db = os.environ.get("REDIS_DB")

_worker_queue = os.environ.get("WORKER_QUEUE")
_worker_name = os.environ.get("WORKER_NAME")


def start_worker():
    redis_ins = Redis(host=_redis_host, port=_redis_port, db=_redis_db)

    with Connection(redis_ins) as redis_conn:
        worker_queue = 'async-jobs' if _worker_queue is None or len(_worker_queue.strip()) == 0 else _worker_queue
        worker_name = f'async-worker-{randrange(1000, 9999)}' if _worker_name is None or len(_worker_name.strip()) == 0 else _worker_name

        w = Worker(worker_queue, name=worker_name, connection=redis_conn)
        w.work()


start_worker()

import os, time

from pathlib import Path
from dotenv import load_dotenv

from redis import Redis
from rq import Queue

worker_prj_dir = Path(__file__).parent.absolute()
worker_prj_env_file = worker_prj_dir / 'rq-worker.env'

if worker_prj_env_file.exists():
    print("Running local dev env, and loading environment variables from file: {0}".format(worker_prj_env_file))
    load_dotenv(worker_prj_env_file)
else:
    print(f'Running in docker, no rq-worker env file: {worker_prj_env_file}')

_redis_host = os.environ.get("REDIS_HOST")
_redis_port = os.environ.get("REDIS_PORT")
_redis_db = os.environ.get("REDIS_DB")

_worker_queue = os.environ.get("WORKER_QUEUE")


def launch_demo_job():
    redis_conn = Redis(host=_redis_host, port=_redis_port, db=_redis_db)
    worker_queue = 'async-jobs' if _worker_queue is None or len(_worker_queue.strip()) == 0 else _worker_queue

    q = Queue(worker_queue, connection=redis_conn)

    job = q.enqueue("demo_job.run_demo_job")

    time.sleep(3)

    print(job.result)

    
if __name__ == '__main__':
    launch_demo_job()

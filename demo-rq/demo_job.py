import os

from redis import StrictRedis

NEXT_DEMO_JOB_ID = "demojobid:next"
LAST_DEMO_JOB_ID = "demojobid:last"

# cache auto expires after 5 minutes
CACHE_TTL_SECONDS = 300


def run_demo_job():
    redis_client = StrictRedis(host=os.environ["REDIS_HOST"], port=os.environ["REDIS_PORT"], db=os.environ["REDIS_DB"])

    next_demo_job_id = str(redis_client.incr(NEXT_DEMO_JOB_ID))
    next_demo_job_sts_key = f'demo-job-sts:{next_demo_job_id}'

    redis_client.hmset(next_demo_job_sts_key, {
        "demo-job-id": next_demo_job_id,
        "demo-job-status": "Executed"
    })

    redis_client.expire(next_demo_job_sts_key, CACHE_TTL_SECONDS)

    redis_client.set(LAST_DEMO_JOB_ID, next_demo_job_id)
    
    return f'demo job executed with id: {next_demo_job_id}'

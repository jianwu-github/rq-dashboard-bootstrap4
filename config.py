import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
local_env = os.path.join(basedir, '.env')

if os.path.exists(local_env):
    print(f'loading local environment variables from {local_env}')
    load_dotenv(os.path.join(basedir, '.env'))
else:
    print("running inside docker ...")


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "flask-rq-dashboard-bootstrap4"
    REDIS_HOST = os.environ.get('REDIS_HOST') or "localhost"
    REDIS_PORT = os.environ.get('REDIS_PORT') or "6379"
    REDIS_DB = os.environ.get('REDIS_DB') or "0"
    RQ_POLL_INTERVAL = os.environ.get('RQ_POLL_INTERVAL') or "2500"

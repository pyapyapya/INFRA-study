import os

import redis
from dotenv import load_dotenv

load_dotenv()

AWS_URL = os.getenv('AWS_URL')

r = redis.Redis(host=AWS_URL, port=6379, db=0)
r.set('key', 'value')

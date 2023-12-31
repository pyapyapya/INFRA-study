import os
import time

import redis
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

AWS_URL = os.getenv('AWS_URL')

class RedisTester:
    def __init__(self):    
        self.redis = redis.StrictRedis(host=AWS_URL, port=6379, db=0, charset='utf-8', decode_responses=True)
        df = pd.read_csv('./titanic.csv').set_index('PassengerId')
        self.df = df.to_dict('index')

    def set(self):
            pipe = self.redis.pipeline()

            start_time = time.time()
            for row in self.df:
                self.redis.hset(name=str(row), mapping=self.df[row])
            pipe.execute()
            end_time = time.time()
            print(f"Pipeline 'set' time operation took {end_time - start_time} seconds")
            return end_time - start_time

    def get(self):
        pipe = self.redis.pipeline()

        start_time = time.time()
        for row in self.df:
            self.redis.hgetall(str(row))
        pipe.execute()
        end_time = time.time()
        print(f"Pipeline 'get' time operation took {end_time - start_time} seconds")
        return end_time - start_time

if __name__ == "__main__":
    test = RedisTester()
    test.set()
    test.get()
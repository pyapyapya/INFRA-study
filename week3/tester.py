from typing import List
from functools import wraps
import time

import matplotlib.pyplot as plt

from rds_test import RDSTester
from redis_test import RedisTester
from dynamodb_test import DynamoDBTester
from redshift_test import RedShiftTester

def timeit(func, verbose=False):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        # first item in the args, ie `args[0]` is `self`
        print(
            f"Function {func.__name__}{(args, kwargs) if verbose else ''} Took {total_time:.4f} seconds"
        )
        return result

    return timeit_wrapper

class Tester:
    def __init__(self, rds_tester: RDSTester, redis_tester: RedisTester, dynamodb_tester: DynamoDBTester, redshift_tester: RedShiftTester):
        self.rds_tester = rds_tester
        self.redis_tester = redis_tester
        self.dynamodb_tester = dynamodb_tester
        self.redshift_tester = redshift_tester

    def test1(self, iterations: int = 1):
        rds_tests = []
        redshift_tests = []
        redis_tests = []
        dynamodb_tests = []

        for i in range(iterations):
            rds_tests.append(self.rds_tester.insert())
            redshift_tests.append(self.redshift_tester.insert())
            redis_tests.append(self.redis_tester.set())
            # dynamodb_tests.append(self.dynamodb_tester.insert())

        self.plot_test(rds_tests, redis_tests, redshift_tests, name="Insert")

    def test2(self, iterations: int = 50):
        # Test set
        rds_tests = []
        redshift_tests = []
        redis_tests = []
        dynamodb_tests = []

        for i in range(iterations):
            rds_tests.append(self.rds_tester.select())
            redshift_tests.append(self.redshift_tester.select())
            redis_tests.append(self.redis_tester.get())
            dynamodb_tests.append(self.dynamodb_tester.select())
        self.plot_test(rds_tests, redis_tests, redshift_tests, dynamodb_tests, name="select")

    def plot_test(self, rds_tests: List[float], redis_tests: List[float], redshift_tests: List[float], dynamodb_tests: List[float], name: str):
        # Plot box plot
        plt.boxplot([rds_tests, redis_tests, redshift_tests, dynamodb_tests])
        plt.xticks([1, 2, 3, 4], ['RDS', 'Redis', 'RedShift', "DynamoDB"])
        plt.ylabel('Time (s)')
        plt.title(name)
        plt.savefig(f'{name}.png')

if __name__ == "__main__":
    rds_tester = RDSTester()
    redis_tester = RedisTester()
    dynamodb_tester = DynamoDBTester()
    redshift_tester = RedShiftTester()
    tester = Tester(rds_tester, redis_tester, dynamodb_tester, redshift_tester)
    # tester.test1()
    tester.test2()
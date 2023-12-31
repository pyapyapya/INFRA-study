import os
import time
from decimal import Decimal
from concurrent.futures import ThreadPoolExecutor

import boto3
import numpy as np
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

class DynamoDBTester:
    def __init__(self):
        profile_name = os.getenv('PROFILE_NAME')
        session = boto3.Session(profile_name=profile_name)
        dynamodb = session.resource('dynamodb', region_name='ap-northeast-3')
        self.table = dynamodb.Table('taehyeon-dynamo')

        df = pd.read_csv('./titanic.csv')
        self.df = df.where(pd.notnull(df), None)
        self.df = self.df.replace({np.nan: None})

    def insert_row(self, row):
        response = self.table.put_item(Item={'taehyeon-partition': str(row["PassengerId"]),
                                                'taehyeon-sort': row["Name"],
                                                'passenger_id': row["PassengerId"],
                                                'survived': row["Survived"],
                                                'pclass': row["Pclass"],
                                                'name': row["Name"],
                                                'Sex': row["Sex"],
                                                # 'Age': Decimal(row["Age"]),
                                                'SibSp': row["SibSp"],
                                                'Parch': row["Parch"],
                                                'Ticket': row["Ticket"],
                                                # 'Fare': Decimal(row["Fare"]),
                                                'Cabin': row["Cabin"],
                                                'Embarked': row["Embarked"]})
        return response

    def insert(self):
        start_time = time.time()

        with ThreadPoolExecutor(max_workers=1) as executor:
            futures = [executor.submit(self.insert_row, row) for idx, row in self.df.iterrows()]
            for future in futures:
                response = future.result()
                print(response)

        end_time = time.time()
        print(f"DynamoDB 'INSERT' operation took {end_time - start_time} seconds")

    def select(self):
        start_time = time.time()
        response = self.table.scan()
        end_time = time.time()

        print(f"DynamoDB 'SELECT' operation took {end_time - start_time} seconds")

        return end_time - start_time



if __name__ == "__main__":
    tester = DynamoDBTester()
    # tester.insert()
    tester.select()
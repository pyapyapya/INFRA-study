import os
import time

import pymysql
import pandas as pd
import numpy as np
from dotenv import load_dotenv

load_dotenv()


class RDSTester:
    def __init__(self):
        username = os.getenv('USERNAME')
        password = os.getenv('PASSWORD')
        host = os.getenv('HOST')
        database = os.getenv('DATABASE')

        self.conn = pymysql.connect(host=host, user=username, password=password, db=database)
        self.titanic = pd.read_csv('titanic.csv')
        self.titanic = self.titanic.where(pd.notnull(self.titanic), None)
        self.titanic = self.titanic.replace({np.nan: None})

    def insert(self):
        start_time = time.time()
        cursor = self.conn.cursor()
        for row in self.titanic.itertuples():
            cursor.execute("INSERT INTO titanic (PassengerID, Survived, Pclass, Name, Sex, Age, SibSp, Parch, Ticket, Fare, Cabin, Embarked) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", row[1:])
        self.conn.commit()
        end_time = time.time()
        print(f"RDS 'INSERT' operation took {end_time - start_time} seconds")
        return end_time - start_time

    def select(self):
        start_time = time.time()
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM titanic")
        rows = cursor.fetchall()
        end_time = time.time()

        print(f"RDS SELECT' operation took {end_time - start_time} seconds")
        return end_time - start_time

if __name__ == "__main__":
    tester = RDSTester()
    tester.insert()
    tester.select()
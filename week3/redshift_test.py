import os
import time

import pandas as pd
import numpy as np

from dotenv import load_dotenv
import redshift_connector

load_dotenv()

class RedShiftTester:
    def __init__(self):
        self.conn = redshift_connector.connect(
            host=os.getenv('REDSHIFT_URL'),
            database='dev',
            user='awsuser',
            password=os.getenv('REDSHIFT_PW'),
            port=5439,
        )
        self.titanic = pd.read_csv('titanic.csv')
        self.titanic = self.titanic.where(pd.notnull(self.titanic), None)
        self.titanic = self.titanic.replace({np.nan: None})

        self.create()

    def create(self):
        cursor = self.conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS titanic")
        cursor.execute("CREATE TABLE titanic (PassengerId INT, Survived INT, Pclass INT, Name VARCHAR(100), Sex VARCHAR(10), Age FLOAT, SibSp INT, Parch INT, Ticket VARCHAR(20), Fare FLOAT, Cabin VARCHAR(20),Embarked CHAR(1))")

    def insert(self):
        start_time = time.time()
        cursor = self.conn.cursor()
        for row in self.titanic.itertuples():
            cursor.execute("INSERT INTO titanic (PassengerID, Survived, Pclass, Name, Sex, Age, SibSp, Parch, Ticket, Fare, Cabin, Embarked) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", row[1:])
        self.conn.commit()
        end_time = time.time()
        print(f"RedShift'INSERT' operation took {end_time - start_time} seconds")
        return end_time - start_time

    def select(self):
        start_time = time.time()
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM titanic")
        cursor.fetchall()
        end_time = time.time()

        print(f"RedShift 'SELECT' operation took {end_time - start_time} seconds")

        return end_time - start_time

if __name__ == "__main__":
    tester = RedShiftTester()
    tester.insert()
    tester.select()
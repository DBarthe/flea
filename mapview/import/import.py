#!/usr/bin/env python3

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

CASSANDRA_ENDPOINT = "localhost"
CASSANDRA_USER = "changme"
CASSANDRA_PASSWORD = "changeme"

class DatabaseAdapter:
    def __init__(self):
        self._cluster = None
        self._session = None

    def configure(self, endpoint, user, password):
        self._authProvider = PlainTextAuthProvider(
            username=user,
            password=password
        )
        self._cluster = Cluster([endpoint], auth_provider=self._authProvider)
        return self

    def connect(self):
        self._session = self._cluster.connect()
        return self

    def shutdown(self):
        self._session.shutdown()
        self._cluster.shutdown()
        return self

    def use(self, keyspace):
        self._session.set_keyspace(keyspace)
        return self

    def execute(self, query, params=None):
        return self._session.execute(query, params)

    def prepare(self, query):
        return self._session.prepare(query)

class StudentManager:
    def __init__(self, adapter):
        self._adapter = adapter
        self._insertStudentStmt = None

    def perpareStatements(self):
        self._insertStudentStmt = slef._adapter.prepare("""
            INSERT INTO student (login, firstname, lastname, email, fc, class)
            VALUES (?, ?, ?, ?, ?, ?);
        """)
        return self

    def insert(self, student):
        self._adapter.execute(self._insertStudentStmt, [
            student.login, student.firstname, student.lastname,
            student.email, student.fc, student.class_
        ])
        return self

class Student:
    def __init__(firstname, lastname, email, fc, class_):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.fc = fc
        self.class_ = class_

    @property
    def login(self):
        try:
            return self.email.strip().split('@')[0].split('.')[1]
        except Exception as e:
            return None

def main():
    adapter = DatabaseAdapter().configure(
        endpoint=CASSANDRA_ENDPOINT,
        user=CASSANDRA_USER,
        password=CASSANDRA_PASSWORD
    )
    adapter.connect().use("mapview")

    manager = Manager().perpareStatements()
    manager.insert(Student(
        firstname="barthelemy",
        lastname="delemotte",
        email="barthelemy.delemotte@univ-lille1.fr",
        fc=False,
        class_="L3 MIAGE"
    ))
    adapter.shutdown()

if __name__ == '__main__':
    main()
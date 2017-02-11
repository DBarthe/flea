#!/usr/bin/env python3

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from lxml import etree
from distutils.util import strtobool
import getpass
import sys

CASSANDRA_ENDPOINT = "localhost"
STUDENTS_FILE = 'students.xml'

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
        self._insertStudentStmt = self._adapter.prepare("""
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

    CLASS_MAP = {
        'Master 2 TIIR': 'M2 TIIR',
        'Master 2 MOCAD': 'M2 MOCAD',
        'Master 2 MIAGE FA-FC': 'M2 MIAGE',
        'Master 2 MIAGE': 'M2 MIAGE',
        'Master 2 IVI': 'M2 IVI',
        'Master 2 IAGL': 'M2 IAGL',
        'Master 2 E-Services': 'M2 E-Services',
        'Master': 'M1 Info',
        'Master 1 MIAGE': 'M1 MIAGE',
        'Master 1 MIAGE FA-FC': 'M1 MIAGE',
        'Licence S5-S6': 'L3 Info',
        'Licence MIAGE': 'L3 MIAGE',
        'Licence S3 - S4': 'L2 Info'
    }

    def __init__(self, firstname, lastname, email, fc, class_):
        self.firstname = firstname
        self.lastname = lastname
        if email == None:
            email = ("%s.%s@etudiant.univ-lille1.fr" % (lastname, firstname)).lower()
        self.email = email
        self.fc = fc
        if Student.CLASS_MAP.has_key(class_):
            self.class_ = Student.CLASS_MAP[class_]
        else:
            self.class_ = class_

    @property
    def login(self):
        try:
            return self.email.strip().split('@')[0].split('.')[1]
        except Exception as e:
            try:
                return self.email.strip().split('@')[0]
            except Exception as e:
                return None

    def __str__(self):
        return ("%s %s %s %d %s" % (
            self.firstname, self.lastname, self.email, self.fc, self.class_
        ))


class XMLParser:
    def __init__(self):
        pass

    def parse(self, filename):
        self._root = etree.parse(filename)
        return self

    def nextStudent(self):
        for studentElement in self._root.xpath('/students/student'):
            yield Student(
                firstname = studentElement.xpath('firstname')[0].text,
                lastname = studentElement.xpath('lastname')[0].text,
                email = studentElement.xpath('email')[0].text,
                class_ = studentElement.xpath('class')[0].text,
                fc = bool(strtobool(studentElement.xpath('fc')[0].text))
            )

def main(argv):

    if len(argv) < 2:
        print ("usage: %s <cassandra_user>" % argv[0])
        exit (1)

    user = argv[1]
    password = getpass.getpass()

    adapter = DatabaseAdapter().configure(
        endpoint=CASSANDRA_ENDPOINT,
        user=user,
        password=password
    )
    adapter.connect().use("fil")

    manager = StudentManager(adapter).perpareStatements()

    parser = XMLParser().parse(STUDENTS_FILE)
    for student in parser.nextStudent():
        if student.login == None:
            print (student)
        else:
            manager.insert(student)

    adapter.shutdown()


if __name__ == '__main__':
    main(sys.argv)

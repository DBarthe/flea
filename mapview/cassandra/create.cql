CREATE KEYSPACE IF NOT EXISTS fil WITH replication = {
  'class': 'SimpleStrategy',
  'replication_factor': 1
};

USE fil;

CREATE TABLE IF NOT EXISTS station (
  building int,
  hostname text,
  login text,
  ts timestamp,
  PRIMARY KEY (building, hostname)
);

CREATE TABLE IF NOT EXISTS report_by_hostname (
  hostname text,
  login text,
  ts timestamp,
  PRIMARY KEY (hostname, login)
);

CREATE TABLE IF NOT EXISTS report_by_login (
  hostname text,
  login text,
  ts timestamp,
  PRIMARY KEY (login, hostname)
);

CREATE TABLE IF NOT EXISTS student (
  login text,
  firstname text,
  lastname text,
  email text,
  class text,
  fc boolean,
  hostname text,
  hostname_ts timestamp,
  PRIMARY KEY (login)
);

CREATE INDEX student_by_class ON student (class);
CREATE INDEX student_by_firstname ON student (firstname);
CREATE INDEX student_by_lastname ON student (lastname);

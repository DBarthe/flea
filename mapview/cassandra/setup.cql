CREATE KEYSPACE IF NOT EXISTS mapview WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1 };

Use mapview;

CREATE TABLE IF NOT EXISTS station (
  hostname text PRIMARY KEY,
  user text,
);

CREATE TABLE IF NOT EXISTS report (
  hostname text,
  user text,
  ts timestamp,
  PRIMARY KEY (user, ts, hostname)
) WITH CLUSTERING ORDER BY (ts DESC);

CREATE TABLE IF NOT EXISTS student (
  login text PRIMARY KEY,
  firstname text,
  lastname text,
  email text,
  class text,
  fc boolean,
  hostname text,
  hostname_ts,
)

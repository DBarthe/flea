CREATE ROLE IF NOT EXISTS mapview_pull;
GRANT SELECT ON KEYSPACE mapview TO mapview_pull;

CREATE ROLE IF NOT EXISTS mapview_push;
GRANT MODIFY ON KEYSPACE mapview to mapview_push;

CREATE ROLE IF NOT EXIST mapview_admin;
GRANT ALL PERMISSIONS ON KEYSPACE mapview;

// CREATE ROLE IF NOT EXISTS mapview_collector WITH LOGIN = true AND password = 'changeme';
// GRANT mapview_push ON mapview_collector

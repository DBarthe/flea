CREATE ROLE IF NOT EXISTS mapview_pull;
GRANT SELECT ON KEYSPACE mapview TO mapview_pull;

CREATE ROLE IF NOT EXISTS mapview_push;
GRANT MODIFY ON KEYSPACE mapview TO mapview_push;

CREATE ROLE IF NOT EXISTS mapview_admin;
GRANT ALL PERMISSIONS ON KEYSPACE mapview TO mapview_admin;

// CREATE ROLE IF NOT EXISTS mapview_collector WITH LOGIN = true AND password = 'changeme'
// GRANT mapview_push ON mapview_collector

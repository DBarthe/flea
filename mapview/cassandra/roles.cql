-- CREATE ROLE IF NOT EXISTS mapview_pull;
-- GRANT SELECT ON KEYSPACE mapview TO mapview_pull;
--
-- CREATE ROLE IF NOT EXISTS mapview_push;
-- GRANT MODIFY ON KEYSPACE mapview TO mapview_push;
--
-- CREATE ROLE IF NOT EXISTS mapview_admin;
-- GRANT ALL PERMISSIONS ON KEYSPACE mapview TO mapview_admin;

// CREATE ROLE IF NOT EXISTS mapview_collector WITH LOGIN = true AND password = 'changeme'
// GRANT mapview_push ON mapview_collector

CREATE ROLE IF NOT EXISTS fil_pull;
GRANT SELECT ON KEYSPACE fil TO fil_pull;

CREATE ROLE IF NOT EXISTS fil_push;
GRANT MODIFY ON KEYSPACE fil TO fil_push;

CREATE ROLE IF NOT EXISTS fil_admin;
GRANT ALL PERMISSIONS ON KEYSPACE fil to fil_admin;

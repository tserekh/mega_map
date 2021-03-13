sudo -u postgres psql postgres
ALTER USER "postgres" WITH PASSWORD 'gyroscope1';
CREATE DATABASE db OWNER postgres;
CREATE DATABASE users OWNER postgres;
CREATE SCHEMA postgres;
CREATE SCHEMA schema_name
\q
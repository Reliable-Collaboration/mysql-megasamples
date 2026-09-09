-- Accounts for the PostgreSQL image (knowledge/decisions/database-naming-convention.md, applied to
-- PostgreSQL). Runs once in the builder stage against the freshly initialised cluster; the official
-- entrypoint never initialises a cluster that already holds PG_VERSION, so nothing here runs at
-- container start. entrypoint-wrapper.sh applies POSTGRES_PASSWORD / DEMO_PASSWORD / ADMIN_PASSWORD
-- overrides at run time.
--
-- `postgres` is the superuser, password `root`, so every engine's superuser answers to the same
-- boilerplate credential. `admin` can do anything short of superuser; `demo` can only read, and
-- 20-grants.sql applies its SELECT grant inside each database as it is created.
ALTER USER postgres WITH PASSWORD 'root';
CREATE ROLE admin WITH LOGIN PASSWORD 'admin' CREATEDB CREATEROLE;
CREATE ROLE demo WITH LOGIN PASSWORD 'demo';

-- the provenance registry: one row per dataset, the same columns as MySQL's megasamples.datasets
CREATE DATABASE megasamples TEMPLATE template0 ENCODING 'UTF8';
GRANT CONNECT ON DATABASE megasamples TO demo, admin;
\connect megasamples
CREATE TABLE datasets (
  name              varchar(64)  NOT NULL PRIMARY KEY,
  tier              varchar(24)  NOT NULL,
  record            varchar(128) NOT NULL,
  upstream_version  varchar(128),
  licenses          json,
  artifacts         json,
  row_counts        json,
  build_id          varchar(64),
  engine            varchar(16)  NOT NULL DEFAULT 'postgres',
  not_ported        json
);
GRANT SELECT ON datasets TO demo;
GRANT ALL ON datasets TO admin;
-- the same schema rights the dataset databases get, so admin can create here too
GRANT USAGE ON SCHEMA public TO demo, admin;
GRANT CREATE ON SCHEMA public TO admin;

-- Run inside each database after its data is loaded: demo reads everything, admin owns nothing but
-- can do anything, and both keep those rights on tables created later.
GRANT USAGE ON SCHEMA public TO demo, admin;
GRANT CREATE ON SCHEMA public TO admin;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO demo;
GRANT ALL ON ALL TABLES IN SCHEMA public TO admin;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO admin;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO demo;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO admin;

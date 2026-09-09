-- Run inside each database after its data is loaded, which happens as `admin`: admin owns every
-- table, view, routine and trigger of the sample databases and can alter or drop them, demo reads
-- everything, and tables admin creates later are readable by demo too.
GRANT USAGE ON SCHEMA public TO demo, admin;
GRANT CREATE ON SCHEMA public TO admin;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO demo;
ALTER DEFAULT PRIVILEGES FOR ROLE admin IN SCHEMA public GRANT SELECT ON TABLES TO demo;

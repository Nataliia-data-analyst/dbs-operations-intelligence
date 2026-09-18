-- ============================================================
-- READ-ONLY ROLE FOR THE AI ANALYTICS AGENT
-- ============================================================

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_roles
        WHERE rolname = 'analyst_ro'
    ) THEN
        CREATE ROLE analyst_ro
            LOGIN
            PASSWORD 'analyst_ro_pwd';
    END IF;
END
$$;


-- Allow the agent to connect to the database.
GRANT CONNECT ON DATABASE operations_intelligence TO analyst_ro;
-- Allow access to objects inside the public schema.
GRANT USAGE ON SCHEMA public TO analyst_ro;

-- Business data can only be read.
GRANT SELECT ON ALL TABLES IN SCHEMA public TO analyst_ro;

-- Future tables should also be readable by default.
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT ON TABLES TO analyst_ro;


-- ============================================================
-- AUDIT LOG
-- ============================================================

-- The agent may add audit records.
GRANT INSERT ON audit_log TO analyst_ro;

-- BIGSERIAL uses a PostgreSQL sequence, so INSERT also needs
-- permission to obtain the next audit_id.
GRANT USAGE, SELECT ON SEQUENCE audit_log_audit_id_seq TO analyst_ro;


-- ============================================================
-- RESTRICTIONS
-- ============================================================

-- The analytics role must not create database objects.
REVOKE CREATE ON SCHEMA public FROM analyst_ro;

-- Protect the database from long-running analytical queries.
ALTER ROLE analyst_ro SET statement_timeout = '15s';

-- Do not allow forgotten transactions to stay open indefinitely.
ALTER ROLE analyst_ro SET idle_in_transaction_session_timeout = '30s';
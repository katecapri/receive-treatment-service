#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
	CREATE TABLE IF NOT EXISTS treatments (
    id UUID DEFAULT gen_random_uuid() NOT NULL,
    last_name VARCHAR NOT NULL,
    first_name VARCHAR NOT NULL,
    patronymic VARCHAR NOT NULL,
    phone VARCHAR NOT NULL,
    treatment VARCHAR NOT NULL,
    creation_date timestamp without time zone NOT NULL DEFAULT clock_timestamp()
	);
	ALTER TABLE treatments OWNER TO postgres_user;
EOSQL
--
-- PostgreSQL database schema
--

-- Dumped from database version 9.6.1
-- Dumped by pg_dump version 9.6.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;

--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

-- the schema

CREATE USER database_user;
ALTER USER database_user PASSWORD 'UnicornCanteloupe';
CREATE DATABASE the_database;
GRANT ALL PRIVILEGES ON DATABASE the_database TO database_user;
\c the_database;


--
-- Name: assets; Type: TABLE; Schema: public; Owner: database_user
--

CREATE TABLE users (
    user_id text NOT NULL,
    username text NOT NULL,
    salt text NOT NULL,
    hash text NOT NULL
);

ALTER TABLE users OWNER TO database_user;

--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: database_user
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (username);

-- PostgreSQL automatically creates a unique index when a unique constraint or primary key is defined for a table.
-- The index covers the columns that make up the primary key or unique constraint (a multicolumn index, if appropriate),
-- and is the mechanism that enforces the constraint.
ALTER TABLE ONLY users
    ADD CONSTRAINT user_id_unique UNIQUE (user_id);

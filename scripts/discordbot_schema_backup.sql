--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

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

--
-- Name: api_token; Type: TABLE; Schema: public; Owner: kebok; Tablespace: 
--

CREATE TABLE api_token (
    id integer NOT NULL,
    api_name character varying(50) NOT NULL,
    token_id character varying(100) NOT NULL,
    created_date timestamp without time zone DEFAULT now() NOT NULL,
    active boolean DEFAULT true NOT NULL
);


ALTER TABLE public.api_token OWNER TO kebok;

--
-- Name: api_token_id_seq; Type: SEQUENCE; Schema: public; Owner: kebok
--

CREATE SEQUENCE api_token_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.api_token_id_seq OWNER TO kebok;

--
-- Name: api_token_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kebok
--

ALTER SEQUENCE api_token_id_seq OWNED BY api_token.id;


--
-- Name: kyoncoin; Type: TABLE; Schema: public; Owner: kebok; Tablespace: 
--

CREATE TABLE kyoncoin (
    id integer NOT NULL,
    server_id character varying(25) NOT NULL,
    user_id character varying(25) NOT NULL,
    coin_amount integer DEFAULT 0 NOT NULL,
    last_updated timestamp without time zone DEFAULT now() NOT NULL,
    active boolean DEFAULT true NOT NULL
);


ALTER TABLE public.kyoncoin OWNER TO kebok;

--
-- Name: kyoncoin_id_seq; Type: SEQUENCE; Schema: public; Owner: kebok
--

CREATE SEQUENCE kyoncoin_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.kyoncoin_id_seq OWNER TO kebok;

--
-- Name: kyoncoin_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kebok
--

ALTER SEQUENCE kyoncoin_id_seq OWNED BY kyoncoin.id;


--
-- Name: math_record; Type: TABLE; Schema: public; Owner: kebok; Tablespace: 
--

CREATE TABLE math_record (
    id integer NOT NULL,
    server_id integer NOT NULL,
    user_id integer NOT NULL,
    success_count integer DEFAULT 0 NOT NULL,
    failed_count integer DEFAULT 0 NOT NULL,
    lastmodified timestamp without time zone DEFAULT now() NOT NULL,
    active boolean DEFAULT true NOT NULL
);


ALTER TABLE public.math_record OWNER TO kebok;

--
-- Name: math_record_id_seq; Type: SEQUENCE; Schema: public; Owner: kebok
--

CREATE SEQUENCE math_record_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.math_record_id_seq OWNER TO kebok;

--
-- Name: math_record_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kebok
--

ALTER SEQUENCE math_record_id_seq OWNED BY math_record.id;


--
-- Name: pkmn_info; Type: TABLE; Schema: public; Owner: kebok; Tablespace: 
--

CREATE TABLE pkmn_info (
    id integer NOT NULL,
    pokedex_id integer NOT NULL,
    name character varying(50) NOT NULL,
    type_one integer NOT NULL,
    type_two integer,
    sprite_ref text
);


ALTER TABLE public.pkmn_info OWNER TO kebok;

--
-- Name: pkmn_info_id_seq; Type: SEQUENCE; Schema: public; Owner: kebok
--

CREATE SEQUENCE pkmn_info_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.pkmn_info_id_seq OWNER TO kebok;

--
-- Name: pkmn_info_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kebok
--

ALTER SEQUENCE pkmn_info_id_seq OWNED BY pkmn_info.id;


--
-- Name: pkmn_type; Type: TABLE; Schema: public; Owner: kebok; Tablespace: 
--

CREATE TABLE pkmn_type (
    id integer NOT NULL,
    name character varying(10) NOT NULL
);


ALTER TABLE public.pkmn_type OWNER TO kebok;

--
-- Name: pkmn_type_id_seq; Type: SEQUENCE; Schema: public; Owner: kebok
--

CREATE SEQUENCE pkmn_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.pkmn_type_id_seq OWNER TO kebok;

--
-- Name: pkmn_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kebok
--

ALTER SEQUENCE pkmn_type_id_seq OWNED BY pkmn_type.id;


--
-- Name: subreddit; Type: TABLE; Schema: public; Owner: kebok; Tablespace: 
--

CREATE TABLE subreddit (
    id integer NOT NULL,
    code character varying(20) NOT NULL,
    url character varying(100) NOT NULL,
    image_only boolean DEFAULT true NOT NULL
);


ALTER TABLE public.subreddit OWNER TO kebok;

--
-- Name: subreddit_id_seq; Type: SEQUENCE; Schema: public; Owner: kebok
--

CREATE SEQUENCE subreddit_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.subreddit_id_seq OWNER TO kebok;

--
-- Name: subreddit_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kebok
--

ALTER SEQUENCE subreddit_id_seq OWNED BY subreddit.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: kebok
--

ALTER TABLE ONLY api_token ALTER COLUMN id SET DEFAULT nextval('api_token_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: kebok
--

ALTER TABLE ONLY kyoncoin ALTER COLUMN id SET DEFAULT nextval('kyoncoin_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: kebok
--

ALTER TABLE ONLY math_record ALTER COLUMN id SET DEFAULT nextval('math_record_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: kebok
--

ALTER TABLE ONLY pkmn_info ALTER COLUMN id SET DEFAULT nextval('pkmn_info_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: kebok
--

ALTER TABLE ONLY pkmn_type ALTER COLUMN id SET DEFAULT nextval('pkmn_type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: kebok
--

ALTER TABLE ONLY subreddit ALTER COLUMN id SET DEFAULT nextval('subreddit_id_seq'::regclass);


--
-- Name: api_token_pkey; Type: CONSTRAINT; Schema: public; Owner: kebok; Tablespace: 
--

ALTER TABLE ONLY api_token
    ADD CONSTRAINT api_token_pkey PRIMARY KEY (id);


--
-- Name: kyoncoin_pkey; Type: CONSTRAINT; Schema: public; Owner: kebok; Tablespace: 
--

ALTER TABLE ONLY kyoncoin
    ADD CONSTRAINT kyoncoin_pkey PRIMARY KEY (id);


--
-- Name: math_record_pkey; Type: CONSTRAINT; Schema: public; Owner: kebok; Tablespace: 
--

ALTER TABLE ONLY math_record
    ADD CONSTRAINT math_record_pkey PRIMARY KEY (id);


--
-- Name: pkmn_info_pkey; Type: CONSTRAINT; Schema: public; Owner: kebok; Tablespace: 
--

ALTER TABLE ONLY pkmn_info
    ADD CONSTRAINT pkmn_info_pkey PRIMARY KEY (id);


--
-- Name: pkmn_type_pkey; Type: CONSTRAINT; Schema: public; Owner: kebok; Tablespace: 
--

ALTER TABLE ONLY pkmn_type
    ADD CONSTRAINT pkmn_type_pkey PRIMARY KEY (id);


--
-- Name: subreddit_pkey; Type: CONSTRAINT; Schema: public; Owner: kebok; Tablespace: 
--

ALTER TABLE ONLY subreddit
    ADD CONSTRAINT subreddit_pkey PRIMARY KEY (id);


--
-- Name: pkmn_info_type_one_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kebok
--

ALTER TABLE ONLY pkmn_info
    ADD CONSTRAINT pkmn_info_type_one_fkey FOREIGN KEY (type_one) REFERENCES pkmn_type(id) ON DELETE RESTRICT;


--
-- Name: pkmn_info_type_two_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kebok
--

ALTER TABLE ONLY pkmn_info
    ADD CONSTRAINT pkmn_info_type_two_fkey FOREIGN KEY (type_two) REFERENCES pkmn_type(id) ON DELETE RESTRICT;


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--


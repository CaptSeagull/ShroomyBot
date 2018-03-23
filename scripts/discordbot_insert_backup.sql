--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

--
-- Data for Name: pkmn_type; Type: TABLE DATA; Schema: public; Owner: kebok
--

INSERT INTO pkmn_type (id, name) VALUES (1, 'normal');
INSERT INTO pkmn_type (id, name) VALUES (2, 'fire');
INSERT INTO pkmn_type (id, name) VALUES (3, 'fighting');
INSERT INTO pkmn_type (id, name) VALUES (4, 'water');
INSERT INTO pkmn_type (id, name) VALUES (5, 'flying');
INSERT INTO pkmn_type (id, name) VALUES (6, 'grass');
INSERT INTO pkmn_type (id, name) VALUES (7, 'poison');
INSERT INTO pkmn_type (id, name) VALUES (8, 'electric');
INSERT INTO pkmn_type (id, name) VALUES (9, 'ground');
INSERT INTO pkmn_type (id, name) VALUES (10, 'psychic');
INSERT INTO pkmn_type (id, name) VALUES (11, 'rock');
INSERT INTO pkmn_type (id, name) VALUES (12, 'ice');
INSERT INTO pkmn_type (id, name) VALUES (13, 'bug');
INSERT INTO pkmn_type (id, name) VALUES (14, 'dragon');
INSERT INTO pkmn_type (id, name) VALUES (15, 'ghost');
INSERT INTO pkmn_type (id, name) VALUES (16, 'dark');
INSERT INTO pkmn_type (id, name) VALUES (17, 'steel');
INSERT INTO pkmn_type (id, name) VALUES (18, 'fairy');
INSERT INTO pkmn_type (id, name) VALUES (19, '???');


--
-- Name: pkmn_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kebok
--

SELECT pg_catalog.setval('pkmn_type_id_seq', 19, true);


--
-- PostgreSQL database dump complete
--


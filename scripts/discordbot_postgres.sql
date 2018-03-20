DROP TABLE IF EXISTS kyoncoin;
CREATE TABLE IF NOT EXISTS kyoncoin (
	id 			 	SERIAL PRIMARY KEY,
	server_id    	VARCHAR(25) NOT NULL,
	user_id      	VARCHAR(25) NOT NULL,
	coin_amount  	INT NOT NULL DEFAULT 0,
	last_updated 	TIMESTAMP NOT NULL DEFAULT NOW(),
	active 		 	BOOLEAN NOT NULL DEFAULT 'true'
);

DROP TABLE IF EXISTS math_record;
CREATE TABLE IF NOT EXISTS math_record (
	id 			 	SERIAL PRIMARY KEY,
	server_id    	VARCHAR(25) NOT NULL,
	user_id      	VARCHAR(25) NOT NULL,
	success_count	INT NOT NULL DEFAULT 0,
	failed_count	INT NOT NULL DEFAULT 0,
	lastModified 	TIMESTAMP NOT NULL DEFAULT NOW(),
	active 		 	BOOLEAN NOT NULL DEFAULT 'true'
);

DROP TABLE IF EXISTS pkmn_type;
CREATE TABLE IF NOT EXISTS pkmn_type (
	id				SERIAL PRIMARY KEY,
	name			VARCHAR(10) NOT NULL
);

DROP TABLE IF EXISTS pkmn_info;
CREATE TABLE IF NOT EXISTS pkmn_info (
	id				SERIAL PRIMARY KEY,
	pokedex_id		INT NOT NULL,
	name			VARCHAR(50) NOT NULL,
	type_one		INT NOT NULL REFERENCES pkmn_type(id) ON DELETE RESTRICT,
	type_two		INT NULL REFERENCES pkmn_type(id) ON DELETE RESTRICT,
	sprite_ref		TEXT NULL
);

INSERT INTO pkmn_type (name) VALUES 
	('normal'), ('fire'), 
	('fighting'), ('water'),
	('flying'), ('grass'),
	('poison'), ('electric'),
	('ground'), ('psychic'),
	('rock'), ('ice'),
	('bug'), ('dragon'),
	('ghost'), ('dark'),
	('steel'), ('fairy'),
	('???')
;

DROP TABLE IF EXISTS api_token;
CREATE TABLE IF NOT EXISTS api_token (
	id				SERIAL PRIMARY KEY,
	api_name		VARCHAR(50) NOT NULL,
	token_id		VARCHAR(100) NOT NULL,
	created_date	TIMESTAMP NOT NULL DEFAULT NOW(),
	active			BOOLEAN NOT NULL DEFAULT 'true'
);
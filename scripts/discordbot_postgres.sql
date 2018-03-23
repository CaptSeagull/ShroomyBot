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

DROP TABLE IF EXISTS subreddit;
CREATE TABLE IF NOT EXISTS subreddit (
    id              SERIAL PRIMARY KEY,
    code            VARCHAR(20) NOT NULL,
    url             VARCHAR(100) NOT NULL,
    image_only      BOOLEAN NOT NULL DEFAULT 'true'
);

INSERT INTO subreddit (code, url, image_only) VALUES
    ('cozy', 'CozyPlaces', true),
    ('yuri', 'wholesomeyuri', true),
    ('wakanda', 'wholesomebpt', true),
    ('slep', 'AnimalsBeingSleepy', true),
    ('kawaii', 'awwnime', true),
    ('awww', 'Awww', true),
    ('aww', 'aww', true),
    ('futaba', 'churchoffutaba', true),
    ('wafu', 'headpats', true),
    ('kyoko', 'ultimatedetective', true),
    ('uguu', 'wholesomeanimemes', true),
    ('chan', 'wholesomegreentext', true),
    ('wikihow', 'disneyvacation', true),
    ('wholesome', 'wholesomememes', true),
    ('butwhy', 'mildlyinfuriating', true),
    ('pikaboo', 'PeepingPooch', true),
    ('hellothere', 'PrequelMemes', true),
    ('javascript', 'ProgrammerHumor', true)
    ;
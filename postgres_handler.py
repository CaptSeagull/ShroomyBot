import psycopg2
import config


class PostgresHandler:
    def __init__(self):
        self.dbname = config.sql_db
        self.username = config.sql_username
        self.password = config.sql_password
        self.host = config.sql_host

    def connect(self):
        return psycopg2.connect(dbname=self.dbname, user=self.username, password=self.password, host=self.host)

    def init_tables(self):
        conn = self.connect()
        with conn:
            with conn.cursor() as curs:
                curs.execute("""
                CREATE TABLE IF NOT EXISTS kyoncoin (
                    id	SERIAL PRIMARY KEY,
                    server_id VARCHAR(25) NOT NULL,
                    user_id VARCHAR(25) NOT NULL,
                    coin_amount INT NOT NULL DEFAULT 0,
                    last_updated TIMESTAMP NOT NULL DEFAULT NOW(),
                    active BOOLEAN NOT NULL DEFAULT 'true');
                    """)
                curs.execute("""
                CREATE TABLE IF NOT EXISTS math_record (
                    id SERIAL PRIMARY KEY,
                    server_id VARCHAR(25) NOT NULL,
                    user_id VARCHAR(25) NOT NULL,
                    success_count INT NOT NULL DEFAULT 0,
                    failed_count INT NOT NULL DEFAULT 0,
                    lastModified TIMESTAMP NOT NULL DEFAULT NOW(),
                    active BOOLEAN NOT NULL DEFAULT 'true');
                    """)
                curs.execute("""
                CREATE TABLE IF NOT EXISTS pkmn_type (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(10) NOT NULL);
                    """)
                curs.execute("""
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
                    ('???');
                    """)
                curs.execute("""
                CREATE TABLE IF NOT EXISTS pkmn_info (
                id SERIAL PRIMARY KEY,
                pokedex_id INT NOT NULL,
                name VARCHAR(50) NOT NULL,
                type_one INT NOT NULL REFERENCES pkmn_type(id) ON DELETE RESTRICT,
                type_two INT NULL REFERENCES pkmn_type(id) ON DELETE RESTRICT,
                sprite_ref TEXT NULL);
                """)

        conn.commit()
        conn.close()


class KyonCoin(PostgresHandler):
    def __init__(self):
        PostgresHandler.__init__(self)
        self.select_coins_query = "select coin_amount from kyoncoin where server_id = %s and user_id = %s"
        self.insert_coins_query = ("insert into kyoncoin (server_id, user_id, coin_amount, active) values "
                                   + "(%s, %s, %s, 'true')")
        self.update_coins_query = "update kyoncoin set coin_amount = %s where server_id=%s and user_id=%s"

    def get_coins(self, server_id, user_id):
        coins = 0
        conn = self.connect()
        with conn:
            with conn.cursor() as curs:
                curs.execute(self.select_coins_query, (server_id, user_id))
                result_one = curs.fetchone()
                conn.rollback()
                if result_one:
                    coins = result_one[0]

        conn.close()
        return coins

    def update_coins(self, server_id, user_id, amount):
        conn = self.connect()
        with conn:
            with conn.cursor() as curs:
                curs.execute(self.select_coins_query, (server_id, user_id))
                result_one = curs.fetchone()
                if result_one:
                    amount += result_one[0]
                    curs.execute(self.update_coins_query, (server_id, user_id, amount))
                else:
                    curs.execute(self.insert_coins_query, (server_id, user_id, amount))
                conn.commit()

        conn.close()

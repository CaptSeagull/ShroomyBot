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


class KyonCoin(PostgresHandler):
    def __init__(self):
        PostgresHandler.__init__(self)
        self.select_coins_query = "select coin_amount from kyoncoin where server_id = %s and user_id = %s"
        self.insert_coins_query = ("insert into kyoncoin (server_id, user_id, coin_amount, active) values "
                                   + "(%s, %s, %s, 'true')")
        self.update_coins_query = "update kyoncoin set coin_amount = %s where server_id=%s and user_id=%s"

    def get_coins(self, server_id, user_id):
        """Retrieves coin amount for a given user in a given server."""
        coins = 0
        conn = self.connect()
        with conn:
            with conn.cursor() as curs:
                curs.execute(self.select_coins_query, (server_id, user_id))
                result_one = curs.fetchone()
                conn.rollback()  # Rollback so table won't be stuck on idle
                if result_one:
                    coins = result_one[0]

        conn.close()
        return coins

    def update_coins(self, server_id, user_id, amount):
        """Adds the coin amount (if exists) on the database for a given user in a given server."""
        conn = self.connect()
        with conn:
            with conn.cursor() as curs:
                curs.execute(self.select_coins_query, (server_id, user_id))
                result_one = curs.fetchone()
                if result_one:
                    amount += result_one[0]
                    curs.execute(self.update_coins_query, (amount, server_id, user_id))
                else:
                    curs.execute(self.insert_coins_query, (server_id, user_id, amount))
                conn.commit()

        conn.close()
        return amount


class PokemonSearch(PostgresHandler):
    def __init__(self):
        PostgresHandler.__init__(self)
        self.select_pkmn_query = ("select "
                                  "pokedex_id, "
                                  "name, "
                                  "(select name from pkmn_type where id = pkmn_info.type_one) as type_one, "
                                  "(select name from pkmn_type where id = pkmn_info.type_two) as type_two, "
                                  "sprite_ref "
                                  "from pkmn_info "
                                  "where (name=%s or pokedex_id=%s)")
        self.select_types_query = "select id, name from pkmn_type"
        self.insert_pkmn_query = ("insert into pkmn_info (pokedex_id, name, type_one, type_two, sprite_ref) values "
                                  + "(%s, %s, %s, %s, %s)")

    def get_pkmn(self, name: str, pokedex: int):
        """Retrieves a pokemon entry on the databse if exists"""
        conn = self.connect()
        pkmn_dict = None
        with conn:
            with conn.cursor() as curs:
                curs.execute(self.select_pkmn_query, (name, pokedex))
                result_one = curs.fetchone()
                if result_one:
                    pkmn_types = [result_one[2], result_one[3]]
                    pkmn_dict = {'pkmn_id': result_one[0],
                                 'pkmn_name': result_one[1],
                                 'pkmn_sprite': result_one[4],
                                 'pkmn_types': [types for types in pkmn_types if types is not None]
                                 }
        conn.rollback()
        conn.close()
        return pkmn_dict

    def save_pkmn_data(self, pkmn_data: dict):
        """Saves pkmn data to database."""
        conn = self.connect()
        with conn:
            with conn.cursor() as curs:
                pkmn_type_one = pkmn_data['pkmn_types'][0] if pkmn_data['pkmn_types'] else "???"
                pkmn_type_two = pkmn_data['pkmn_types'][1] if len(pkmn_data['pkmn_types']) > 1 else None
                curs.execute(self.select_types_query)
                pkmn_types = {types[1]: types[0] for types in curs.fetchall()}
                conn.rollback()
                curs.execute(self.insert_pkmn_query,
                             (pkmn_data['pkmn_id'],
                              pkmn_data['pkmn_name'],
                              pkmn_types[pkmn_type_one],
                              pkmn_types[pkmn_type_two] if pkmn_type_two is not None else None,
                              pkmn_data['pkmn_sprite']))
                conn.commit()
        conn.close()

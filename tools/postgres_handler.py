import psycopg2
import tools
import logging


class PostgresHandler:
    def connect(self):
        return psycopg2.connect(tools.get_postgress_sql_url(), sslmode='require')


class Subreddit(PostgresHandler):
    def __init__(self):
        PostgresHandler.__init__(self)
        self.select_img_query = "select code, url from subreddit where image_only = 'true'"

    def get_image_subreddits(self):
        query_subreddits = {}
        try:
            conn = self.connect()
            with conn:
                with conn.cursor() as curs:
                    curs.execute(self.select_img_query)
                    rows = curs.fetchall()
                    conn.rollback()
                    for row in rows:
                        query_subreddits[row[0]] = row[1]

            conn.close()
        except Exception:
            logging.exception("Exception when trying to retrieve image subreddits")
        if query_subreddits:
            tools.subreddits.update(query_subreddits)


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
        try:
            conn = self.connect()
            with conn:
                with conn.cursor() as curs:
                    curs.execute(self.select_coins_query, (str(server_id), str(user_id)))
                    result_one = curs.fetchone()
                    conn.rollback()  # Rollback so table won't be stuck on idle
                    if result_one:
                        coins = result_one[0]

            conn.close()
        except Exception:
            logging.exception("Exception when trying to retrieve kyoncoins")
        return coins

    def update_coins(self, server_id, user_id, amount):
        """Adds the coin amount (if exists) on the database for a given user in a given server."""
        try:
            conn = self.connect()
            with conn:
                with conn.cursor() as curs:
                    curs.execute(self.select_coins_query, (str(server_id), str(user_id)))
                    result_one = curs.fetchone()
                    if result_one:
                        amount += result_one[0]
                        curs.execute(self.update_coins_query, (amount, str(server_id), str(user_id)))
                    else:
                        curs.execute(self.insert_coins_query, (str(server_id), str(user_id), amount))
                    conn.commit()

            conn.close()
        except Exception as e:
            logging.exception("Exception when trying to update kyon coins")
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
        pkmn_dict = None
        try:
            conn = self.connect()
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
        except Exception:
            logging.exception("Exception when trying to retrieve pkmn")
        return pkmn_dict

    def save_pkmn_data(self, pkmn_data: dict):
        """Saves pkmn data to database."""
        try:
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
        except Exception:
            logging.exception("Exception when trying to save pkmn info to db")


class Token(PostgresHandler):
    def __init__(self):
        PostgresHandler.__init__(self)
        self.select_token_query = "select token_id, created_date, active from api_token where api_name = %s"
        self.insert_token_query = "insert into api_token (token_id, api_name) values (%s, %s)"
        self.update_token_query = ("update api_token set token_id = %s, "
                                   + "created_date = now(), "
                                   + "active = \'true\' "
                                   + "where api_name = %s")
        self.update_token_inactive_query = "update api_token set active = \'false\' where api_name = %s"

    def get_token(self, name: str):
        """Retrieves any token value of the api on the database (if any)."""
        result_token, result_date = None, None
        try:
            conn = self.connect()
            with conn:
                with conn.cursor() as curs:
                    curs.execute(self.select_token_query, (name,))
                    result_query = curs.fetchone()
                    conn.rollback()
                    if result_query and result_query[2]:
                        result_token, result_date = result_query[0], result_query[1]
            conn.close()
        except Exception:
            logging.exception("Exception when trying to retrieve {} token".format(name))
        return result_token, result_date

    def update_token(self, name: str, token_id: str):
        """Updates the token value of the api on the database. Creates an entry if not exist yet."""
        try:
            conn = self.connect()
            with conn:
                with conn.cursor() as curs:
                    curs.execute(self.select_token_query, (name,))
                    result_query = curs.fetchone()
                    conn.rollback()
                    if result_query:
                        curs.execute(self.update_token_query, (token_id, name))
                    else:
                        curs.execute(self.insert_token_query, (token_id, name))
                    conn.commit()
            conn.close()
        except Exception:
            logging.exception("Exception when trying to update {} token".format(name))

    def inactive_token(self, name: str):
        """Sets the given api on the database inactive so next time api is called,
         it will need to generate a new one."""
        try:
            conn = self.connect()
            with conn:
                with conn.cursor() as curs:
                    curs.execute(self.update_token_inactive_query, (name,))
                    conn.commit()
            conn.close()
        except Exception as e:
            logging.exception("Exception when trying to inactive {} token".format(name))

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

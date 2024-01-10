import asyncpg
import sqlite3

class Database:
    def __init__(self, db_name):
        self.connector = sqlite3.connect(db_name)
        self.cursor = self.connector.cursor()
        self.create_db()

    def add_user(self, user_name, user_phone, telegram_id):
        query = f"INSERT INTO users (user_name, user_phone, telegram_id)" \
                f"VALUES ('{user_name}', '{user_phone}', '{telegram_id}')"
        self.connector.execute(query)
        self.connector.commit()

    def add_game(self, place_id, date_game, time_game, min_player, max_player, price):
        self.cursor.execute(f'INSERT INTO games(place_id, date_game, time_game,'
                            f'min_player, max_player, price) VALUES ('
                            f'"{place_id}", "{date_game}", "{time_game}",'
                            f' "{min_player}", "{max_player}", "{price}")')
        self.connector.commit()

    def select_user_id(self, tel_id):
        users = self.cursor.execute(f"SELECT * FROM users WHERE telegram_id = '{tel_id}'")
        return users.fetchone()

    def db_select_column(self, table_name, column, item):
        res = self.cursor.execute(f"SELECT * FROM {table_name} WHERE {column} = {item}")
        return res

    def db_select_all(self, table_name):
        result = self.cursor.execute(f'SELECT * FROM {table_name}')
        return result.fetchall()

    def select_games(self, status, date_game):
        res = self.cursor.execute(f"SELECT * FROM games JOIN place "
                                  f"ON games.place_id = place.id WHERE games.status = '{status}' "
                                  f"AND games.date_game = '{date_game}'")
        return res.fetchall()

    def select_game(self, status, game_id):
        res = self.cursor.execute(f"SELECT * FROM games JOIN place "
                                  f"ON games.place_id = place.id WHERE games.status = '{status}' "
                                  f"AND games.id = '{game_id}'")
        return res.fetchone()

    def add_user_match(self, game_id, user_telegram_id):
        self.cursor.execute(f"INSERT INTO record_matchs (game_id, user_telegram_id) "
                            f"VALUES ('{game_id}', '{user_telegram_id}')")
        self.connector.commit()

    def del_user_match(self, game_id, user_telegram_id):
        self.cursor.execute(f"DELETE FROM record_matchs WHERE game_id = '{game_id}' AND "
                            f"user_telegram_id = '{user_telegram_id}'")
        self.connector.commit()

    def select_player(self, game_id):
        res = self.cursor.execute(f"SELECT * FROM record_matchs JOIN users ON "
                                  f"record_matchs.user_telegram_id = users.telegram_id "
                                  f"WHERE record_matchs.game_id = '{game_id}'")
        return res.fetchall()

    def check_user(self, game_id, user_id):
        res = self.cursor.execute(f"SELECT * FROM record_matchs WHERE game_id = '{game_id}' AND "
                                  f"user_telegram_id = '{user_id}'")
        return res.fetchall()

    def user_game(self, status, user_id):
        self.cursor.execute(f"SELECT record_matchs.game_id, record_matchs.user_telegram_id, "
                            f"games.id AS games_id, games.place_id, games.date_game, games.time_game, "
                            f"games.price, games.status, place.id AS places_id, "
                            f"place.name_place, place.place_address "
                            f"FROM record_matchs JOIN games ON record_matchs.game_id = games_id "
                            f"JOIN place ON games.place_id = places_id "
                            f"WHERE games.status = '{status}' AND record_matchs.user_telegram_id = '{user_id}'")
        res = self.cursor.fetchall()
        return res

    def balance_user_edit(self, user_id, balance):
        self.cursor.execute(f"UPDATE users SET balance = '{balance}' WHERE telegram_id = '{user_id}'")
        self.connector.commit()

    def balance_system(self, operation, user_id):
        self.cursor.execute(f"INSERT INTO balance_system (operation, user_id) "
                            f"VALUES ('{operation}', '{user_id}')")
        self.connector.commit()

    def buy_game(self, game_id, user_id, sum):
        self.cursor.execute(f"INSERT INTO paid_game (game_id, user_telegram_id, sum) "
                            f"VALUES ('{game_id}', '{user_id}', '{sum}')")
        self.connector.commit()

    def select_pay(self, game_id, user_id):
        self.cursor.execute(f"SELECT * FROM paid_game WHERE game_id = '{game_id}' "
                            f"AND user_telegram_id = '{user_id}'")
        res = self.cursor.fetchone()
        return res

    def subscr_edit(self, user_id, sub):
        self.cursor.execute(f"UPDATE users SET subscription = '{sub}' WHERE telegram_id = '{user_id}'")
        self.connector.commit()

    def create_db(self):
        try:
            query = f'CREATE TABLE IF NOT EXISTS users(' \
                    f'id INTEGER PRIMARY KEY,' \
                    f'user_name TEXT,' \
                    f'user_phone TEXT,' \
                    f'telegram_id TEXT);' \
                    f'CREATE TABLE IF NOT EXISTS place(' \
                    f'id INTEGER PRIMARY KEY,' \
                    f'name_place TEXT,' \
                    f'place_address TEXT);' \
                    f'CREATE TABLE IF NOT EXISTS games(' \
                    f'id INTEGER PRIMARY KEY,' \
                    f'place_id TEXT,' \
                    f'date_game TEXT,' \
                    f'time_game TEXT,' \
                    f'min_player INTEGER,' \
                    f'max_player INTEGER,' \
                    f'price TEXT)'
            self.cursor.executescript(query)
            self.connector.commit()
        except sqlite3.Error as Error:
            print("Ошибка при создании:", Error)

    def __del__(self):
        self.cursor.close()
        self.connector.close()
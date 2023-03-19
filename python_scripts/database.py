import psycopg2
from typing import List

class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None


    def connect_database(self):
        self.conn = psycopg2.connect(dbname="postgres",
                            host="localhost",
                            user="postgres",
                            password="",
                            port="5435")
        self.cursor = self.conn.cursor()


    def init_database(self):
        self.cursor.execute("""CREATE TABLE tokens_index (
                        token TEXT PRIMARY KEY,
                        indexed_files TEXT[]
                        );""")
        self.conn.commit()

    def close(self):
        self.conn.close()

    def clear_table(self):
        self.cursor.execute("""DROP TABLE tokens_index;""")
        self.conn.commit()


    def add_to_db(self, token: str, files_list: List[str]):
        self.cursor.execute("""INSERT INTO tokens_index (token, indexed_files)
                        VALUES (%s, %s); """,
                        (token, files_list))
        self.conn.commit()
        self.cursor.execute("SELECT * FROM tokens_index WHERE token = '{0}';".format(token))

    def get_token_files(self, token: str) -> List[str]:
        self.cursor.execute("SELECT indexed_files FROM tokens_index WHERE token = '{0}';".format(token))
        return self.cursor.fetchone()
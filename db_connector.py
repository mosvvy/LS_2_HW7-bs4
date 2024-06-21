import sqlite3


class SQLiteConnector:
    def __init__(self, path:str='db.db'):
        self.__path = path
        self.__connection = sqlite3.connect(self.__path)
        self.__cursor = self.__connection.cursor()

    @property
    def cursor(self):
        return self.__cursor

    def exec(self, query: str):
        return self.__cursor.execute(query)

    def commit(self):
        self.__connection.commit()

    def __del__(self):
        self.__cursor.close()
        self.__connection.close()


def create_table_parce_data_phones():
    con = SQLiteConnector('db.db')

    con.cursor.execute("""
    CREATE TABLE IF NOT EXISTS phones(
        id integer primary key autoincrement,
        title text,
        price_range text,
        screen text,
        camera text,
        video text,
        space text,
        processor text,
        ram text,
        battery text,
        corpus text
    );
    """)

    del con


if __name__ == '__main__':
    # create_table_parce_data_phones()

    con = SQLiteConnector()

    con.exec("SELECT * FROM phones")
    r = con.cursor.fetchall()
    for i in r:
        print(i)

    # con.exec("DROP TABLE users")

    del con


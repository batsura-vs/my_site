import sqlite3


class ConnectDB:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)

    def __enter__(self) -> 'cursor':
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.connection.commit()
        self.connection.close()

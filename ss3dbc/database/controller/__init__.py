import sqlite3
from typing import Optional
from ss3dbc.database.table import Table


class Controller:
    __connection: sqlite3.Connection
    __cursor: sqlite3.Cursor

    def __init__(self, location: str):
        self.__connection = sqlite3.connect(location)
        self.__cursor = self.__connection.cursor()

    def __del__(self):
        self.__cursor.close()

    @property
    def tables(self) -> list:
        tables = []

        for table in self.__cursor.execute("SELECT query FROM sqlite_master WHERE type='table';"):
            tables.append(self.get_table(table[0]))

        return tables

    def get_table(self, name: str) -> Optional[Table]:
        return Table(name, self)

    def create_table(self, name: str, query: str):
        self.__cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {name} (id INT NOT NULL UNIQUE PRIMARY KEY, {query});"
        )
        self.__connection.commit()
        return self.get_table(name)

    def delete_table(self, name: str):
        self.__cursor.execute(f"DROP TABLE {name};")
        self.__connection.commit()

    def query(self, query: str) -> sqlite3.Cursor:
        return self.__cursor.execute(f"{query}")

    def execute(self, query: str):
        self.__cursor.execute(f"{query}")
        self.__connection.commit()

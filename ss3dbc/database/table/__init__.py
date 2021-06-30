from ss3dbc.database.table.line import Line
from ss3dbc.database.table.line.date import Date


# cannot import because import problem
class Controller: ...


# noinspection PyUnresolvedReferences
class Table:
    __name: str
    __controller: Controller

    def __init__(self, name: str, controller: Controller):
        self.__name = name
        self.__controller = controller

    @property
    def name(self) -> str:
        return self.__name

    @property
    def controller(self) -> Controller:
        return self.__controller

    @property
    def data(self):
        result = []
        data = self.__controller.query(f"SELECT * FROM {self.name}").fetchall()

        for record in data:
            result.append(Line(record[0], self))

        return result

    @property
    def columns(self):
        columns = []
        data = self.controller.query(f"SELECT * FROM {self.name}")

        for column in data.description:
            columns.append(column[0])

        return columns

    def add_column(self, query: str):
        self.controller.execute(f"ALTER TABLE {self.name} ADD {query};")

    def update_column_type(self, query: str, new_type: str):
        self.controller.execute(f"ALTER TABLE {self.name} ALTER COLUMN {query} {new_type};")

    def delete_column(self, query: str):
        self.controller.execute(f"ALTER TABLE {self.name} DROP COLUMN {query};")

    def add_record(self, query: str):
        id = 0

        for line in self.data:
            if line.id >= id:
                id = line.id + 1

        self.controller.execute(f"INSERT INTO {self.name} ({', '.join(self.columns)}) VALUES ({id}, {query});")

    def update_record(self, old_query: str, new_query: str):
        self.controller.execute(f"UPDATE {self.name} SET {new_query} WHERE {old_query};")

    def delete_record(self, query: str):
        self.controller.execute(f"DELETE FROM {self.name} WHERE {query};")

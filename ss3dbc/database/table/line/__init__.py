class Table: ...


# noinspection PyUnresolvedReferences
class Line:
    __line_id: int
    __column: list
    __table: Table

    def __init__(self, line_id: int, table: Table):
        self.__line_id = line_id
        self.__table = table

    @property
    def columns(self) -> list:
        return self.table.columns

    @property
    def table(self) -> Table:
        return self.__table

    @property
    def id(self):
        return self.__line_id

    @property
    def data(self) -> dict:
        data = {}
        # noinspection SqlResolve
        line_data = self.table.controller.query(
            f"SELECT * FROM {self.table.name} WHERE id={self.__line_id};").fetchone()

        for index in range(len(line_data)):
            data[self.columns[index]] = line_data[index]

        return data

    def update(self, query: str):
        self.table.update_record(f"id={self.id}", f"{query}")

    def delete(self):
        self.table.delete_record(f"id={self.id}")

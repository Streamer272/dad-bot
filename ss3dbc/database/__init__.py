import sqlite3
# from database.controller import Controller
from ss3dbc.database.controller import Controller


class Database(Controller):
    __location: str

    def __init__(self, location=None):
        super().__init__(location)
        self.__location = location

    def __del__(self):
        super().__del__()

    @property
    def location(self) -> str:
        return self.__location

    def close(self):
        super().__del__()
